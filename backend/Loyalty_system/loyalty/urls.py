from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyProgramViewSet, PointBalanceViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'loyalty-programs', LoyaltyProgramViewSet)
router.register(r'point-balances', PointBalanceViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
