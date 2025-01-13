from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import LoyaltyProgram, PointBalance, Transaction
from .serializers import LoyaltyProgramSerializer, PointBalanceSerializer, TransactionSerializer
from .services import redeem_points, earn_points


class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer


class PointBalanceViewSet(viewsets.ModelViewSet):
    queryset = PointBalance.objects.all()
    serializer_class = PointBalanceSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

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


class PointsViewSet(ViewSet):
    def create(self, request):
        action = request.query_params.get('action')  # /points/?action=earn or redeem
        user_id = request.data.get('user_id')
        program_id = request.data.get('program_id')
        points = request.data.get('points')  # Accept 'amount' instead of 'points'

        try:
            if action == "earn":
                balance = earn_points(user_id, program_id, points)
                message = "Points earned"
            elif action == "redeem":
                balance = redeem_points(user_id, program_id, points)
                message = "Points redeemed"
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": message, "balance": balance.balance}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


