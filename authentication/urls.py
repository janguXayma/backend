from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import (
    RegisterView, 
    UserProfileView,
    TokenObtainPairView,
    GoogleLogin,
    UserDetailView)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/auth/user/', UserDetailView.as_view(), name='user_detail'),

    # Route pour Google Login
    path('login/google/', GoogleLogin.as_view(), name='google_login'),
]

    # path('api/google/validate_token/', validate_google_token, name='validate_token'),
    # path('callback/', google_login_callback, name='callback'),