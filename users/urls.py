from django.urls import path
from .views import UserSignupView
# , EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/token/', TokenObtainPairView.as_view(), name='login_token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='login_token_refresh'),
    # path('editProfile/', UserEditProfileView.as_view(), name='user_editProfile'),
]