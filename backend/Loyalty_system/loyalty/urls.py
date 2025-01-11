from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyProgramViewSet, PointBalanceViewSet, TransactionViewSet, PointsViewSet

router = DefaultRouter()
router.register(r'loyalty-programs', LoyaltyProgramViewSet)
router.register(r'point-balances', PointBalanceViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'points', PointsViewSet, basename='points')

urlpatterns = [
    path('api/', include(router.urls)),
]
