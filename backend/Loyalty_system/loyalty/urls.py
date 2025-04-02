from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from .views import LoyaltyProgramViewSet, PointBalanceViewSet, TransactionViewSet, PointsViewSet, LoyaltyTierViewSet, \
    UserTaskProgressViewSet, SpecialTaskViewSet, RegisterView, LoginView, LogoutView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Loyalty System API",
        default_version='v1',
        description="API documentation for the Loyalty System project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'loyalty-programs', LoyaltyProgramViewSet)
router.register(r'point-balances', PointBalanceViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'points', PointsViewSet, basename='points')
router.register(r'loyalty-tiers', LoyaltyTierViewSet)
router.register(r'special-tasks', SpecialTaskViewSet, basename='special-task')
router.register(r'user-task-progress', UserTaskProgressViewSet, basename='user-task-progress')


urlpatterns = [
    path('api/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('/api/register/', RegisterView.as_view(), name='register'),  #  Register
    path('/api/login/', LoginView.as_view(), name='login'),
    path('/api/logout/', LogoutView.as_view(), name='logout'),  #  Logout
]
