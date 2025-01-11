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
        """Override list to filter transactions by user_id."""
        user_id = request.query_params.get('user_id')

        if user_id:
            transactions = Transaction.objects.filter(user_id=user_id)
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Default to the original list behavior if no user_id is provided
        return super().list(request, *args, **kwargs)


class PointsViewSet(ViewSet):
    def create(self, request):
        action = request.query_params.get('action')  # Example: /points/?action=earn
        user_id = request.data.get('user_id')
        program_id = request.data.get('program_id')
        points = request.data.get('points')

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


