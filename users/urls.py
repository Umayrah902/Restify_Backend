from django.urls import path
from .views import UserSignupView, UserEditProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = "users"
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/token/', TokenObtainPairView.as_view(), name='login_token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='login_token_refresh'),
    path('editProfile/', UserEditProfileView.as_view(), name='user_editProfile'),
    path('logout/', TokenBlacklistView.as_view(), name='user_logout'),
]