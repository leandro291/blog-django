from django.urls import path
from users.api.views import RegisterView, UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', UserView.as_view(), name="me"),
]

