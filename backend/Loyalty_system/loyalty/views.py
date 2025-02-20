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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]


class LoyaltyTierViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTier.objects.all()
    serializer_class = LoyaltyTierSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]

class PointBalanceViewSet(viewsets.ModelViewSet):
    queryset = PointBalance.objects.all()
    serializer_class = PointBalanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]
    def list(self, request, *args, **kwargs):
        """Override list to filter point balances by user_id and program_id."""
        user_id = request.query_params.get('user_id')  # Query param for user ID
        program_id = request.query_params.get('program_id')  # Query param for program ID

        # Ensure both parameters are provided
        if not user_id or not program_id:
            return Response(
                {"error": "Both user_id and program_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter point balance by user_id and program_id
        try:
            point_balance = PointBalance.objects.get(user_id=user_id, program_id=program_id)
            serializer = self.get_serializer(point_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PointBalance.DoesNotExist:
            return Response(
                {"error": "Point balance not found for the given user and program."},
                status=status.HTTP_404_NOT_FOUND
            )

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfLoyaltyProgram]
    def list(self, request, *args, **kwargs):
        """Override list to filter transactions by user_id, program_id, and date range."""
        user_id = request.query_params.get('user_id')
        program_id = request.query_params.get('program_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Check if program_id is provided
        if not program_id:
            return Response(
                {"error": "Program ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Build a query dynamically
        filters = Q()
        if user_id:
            filters &= Q(user_id=user_id)
        if program_id:
            filters &= Q(program_id=program_id)
        if start_date and end_date:
            filters &= Q(timestamp__range=[start_date, end_date])
        elif start_date:
            filters &= Q(timestamp__gte=start_date)
        elif end_date:
            filters &= Q(timestamp__lte=end_date)

        # Apply the filters
        transactions = Transaction.objects.filter(filters)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def create_and_update_task_progress(self, request):
        """
        Custom action to create a transaction and automatically check task progress.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()  # Save the transaction

        # Update user task progress after transaction creation
        update_task_progress_for_transaction(transaction)

        return Response(
            {"message": "Transaction created and progress checked!", "transaction": serializer.data},
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