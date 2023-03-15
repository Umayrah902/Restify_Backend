from django.urls import path
from .views import UserSignupView, ViewGuestsView, GuestsReviewsView, GuestPostReviewView
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
    path('guests/', ViewGuestsView.as_view(), name="view_guests_view"),
    path('guests/<int:pk>/', GuestsReviewsView.as_view(), name="guests_reviews_view"),
    path('guests/<int:pk>/review/', GuestPostReviewView.as_view(), name="guest_post_review_view"),
]