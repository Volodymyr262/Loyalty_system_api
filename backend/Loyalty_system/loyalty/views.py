from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, status, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwnerOfLoyaltyProgram
from .models import LoyaltyProgram, PointBalance, Transaction, LoyaltyTier, UserTaskProgress, SpecialTask
from .serializers import LoyaltyProgramSerializer, PointBalanceSerializer, TransactionSerializer, LoyaltyTierSerializer, \
    UserTaskProgressSerializer, SpecialTaskSerializer, UserSerializer
from .services import redeem_points, earn_points, update_task_progress_for_transaction


class RegisterView(generics.CreateAPIView):
    """
     Public view for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  #  Registration is open to everyone

class LoginView(ObtainAuthToken):
    """
     Public view for user login.
    """
    permission_classes = [permissions.AllowAny]  #  Login is open to everyone

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user.id, 'username': token.user.username})


class LogoutView(APIView):
    """
        Logout a user by deleting their authentication token.
       """
    permission_classes = [IsAuthenticated]  #  Only logged-in users can logout

    def post(self, request):
        """  Deletes the user's token and logs them out """
        try:
            request.user.auth_token.delete()  # Delete the user's token
            return Response({"message": "Successfully logged out."}, status=200)
        except:
            return Response({"error": "Something went wrong."}, status=400)


class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer
    permission_classes = [IsOwnerOfLoyaltyProgram]

    def get_queryset(self):
        return LoyaltyProgram.objects.all()  # Remove owner filtering here

    def get_object(self):
        """ Ensure object exists and check ownership before returning """
        obj = super().get_object()

        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this Loyalty Program.")

        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LoyaltyTierViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTier.objects.all()
    serializer_class = LoyaltyTierSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]

    def perform_create(self, serializer):
        """Automatically set the loyalty program based on request data."""
        program_id = self.request.data.get("program")  # Extract program ID
        if not program_id:
            raise serializers.ValidationError({"program": "This field is required."})

        try:
            program = LoyaltyProgram.objects.get(id=program_id, owner=self.request.user)
        except LoyaltyProgram.DoesNotExist:
            raise serializers.ValidationError({"program": "Invalid program or you do not have permission."})

        serializer.save(program=program)  #  Set program before saving

class PointBalanceViewSet(viewsets.ModelViewSet):
    queryset = PointBalance.objects.all()
    serializer_class = PointBalanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]


    def list(self, request, *args, **kwargs):
        """Filter by user_id and program_id and return 404 if not found."""
        user_id = request.query_params.get('user_id')
        program_id = request.query_params.get('program_id')

        if not user_id or not program_id:
            return Response({"error": "Both user_id and program_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the loyalty program exists and belongs to the current user
        if not PointBalance.objects.filter(program_id=program_id, program__owner=request.user).exists():
            return Response({"error": "Unauthorized or invalid program."}, status=status.HTTP_403_FORBIDDEN)

        try:
            point_balance = PointBalance.objects.get(user_id=user_id, program_id=program_id)
            serializer = self.get_serializer(point_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PointBalance.DoesNotExist:
            return Response({"error": "Point balance not found."}, status=status.HTTP_404_NOT_FOUND)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Handles transactions where users earn or redeem points.
    Transactions can be filtered by user_id, program_id, and date range.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]

    def get_queryset(self):
        """
        Filters transactions based on user_id, program_id, and optional date range.
        Ensures only the owner of the loyalty program can access transactions.
        """
        user = self.request.user
        queryset = super().get_queryset()

        # Ensure program_id is provided
        program_id = self.request.query_params.get("program_id")
        if not program_id:
            return Transaction.objects.none()  # No program_id, return empty queryset

        # Check if the current user is the owner of the program
        try:
            program = LoyaltyProgram.objects.get(id=program_id)
            if program.owner != user:
                raise PermissionDenied(
                    "You do not have permission to view these transactions.")  # 🚨 Explicitly deny access
        except LoyaltyProgram.DoesNotExist:
            raise PermissionDenied("Program not found.")  # 🚨 Deny access if program doesn't exist

        # Apply filters if user is the owner
        filters = {"program_id": program_id}
        user_id = self.request.query_params.get("user_id")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if user_id:
            filters["user_id"] = user_id
        if start_date and end_date:
            filters["timestamp__range"] = [start_date, end_date]
        elif start_date:
            filters["timestamp__gte"] = start_date
        elif end_date:
            filters["timestamp__lte"] = end_date

        return queryset.filter(**filters)

    @action(detail=False, methods=["post"])
    def create_and_update_task_progress(self, request):
        """
        Creates a transaction and automatically checks user task progress.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        # Update related user task progress
        update_task_progress_for_transaction(transaction)

        return Response(
            {"message": "Transaction created and progress updated!", "transaction": serializer.data},
            status=status.HTTP_201_CREATED
        )

class PointsViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling point-related actions (earn/redeem points).
    """
    queryset = PointBalance.objects.all()
    serializer_class = PointBalanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]
    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle earn/redeem actions via `action` query parameter.
        """
        action = request.query_params.get('action')  # /points/?action=earn or redeem
        user_id = request.data.get('user_id')
        program_id = request.data.get('program_id')
        points = request.data.get('points')  # Accept 'points'

        try:
            if action == "earn":
                balance = earn_points(user_id, program_id, points)
                message = "Points earned"
            elif action == "redeem":
                balance = redeem_points(user_id, program_id, points)
                message = "Points redeemed"
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"message": message, "balance": balance.balance},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class SpecialTaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Special Tasks.
    Supports CRUD operations and filtering by program_id.
    """
    queryset = SpecialTask.objects.all()
    serializer_class = SpecialTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]
    def get_queryset(self):
        """
        Filter tasks by program_id if provided in query parameters.
        """
        queryset = super().get_queryset()
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        return queryset


class UserTaskProgressViewSet(viewsets.ModelViewSet):
    queryset = UserTaskProgress.objects.all()
    serializer_class = UserTaskProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]

    def create(self, request, *args, **kwargs):
        """
        Create or update progress for a user on a specific task.
        """
        user_id = request.data.get('user_id')
        task_id = request.data.get('task')

        if not user_id or not task_id:
            return Response({"error": "user_id and task are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = SpecialTask.objects.get(id=task_id)
        except SpecialTask.DoesNotExist:
            return Response({"error": f"Task with id {task_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Get or create progress entry
        progress, created = UserTaskProgress.objects.get_or_create(user_id=user_id, task=task)

        # Update progress details
        serializer = self.get_serializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        progress = serializer.save()

        # **Ensure `reward_user()` is called**
        progress.reward_user()  # This will now always check if the task is completed

        return Response(
            self.get_serializer(progress).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update progress and check for task completion.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        progress = serializer.save()

        # Check for task completion after update
        progress.reward_user()

        # Get fresh data from database to include any updates made by reward_user()
        progress.refresh_from_db()

        return Response(self.get_serializer(progress).data)