from django.urls import path

from .views import UserSignupView, UserEditProfileView, UserViewMyProfile, UserDeleteAvatarView, UserViewPublicProfile, ViewGuestsView, GuestsReviewsView, GuestPostReviewView, ViewProfile

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
    path('guests/', ViewGuestsView.as_view(), name="view_guests_view"),
    path('guests/<int:pk>/', GuestsReviewsView.as_view(), name="guests_reviews_view"),
    path('guests/<int:pk>/review/', GuestPostReviewView.as_view(), name="guest_post_review_view"),
    path('viewMyProfile/', UserViewMyProfile.as_view(), name='user_viewProfile'),
    path('editProfile/', UserEditProfileView.as_view(), name='user_editProfile'),
    path('editProfile/deleteAvatar/', UserDeleteAvatarView.as_view(), name='user_editProfile_deleteAvatar'),
    path('logout/', TokenBlacklistView.as_view(), name='user_logout'),
    path('viewPublicProfile/<str:email>/', UserViewPublicProfile.as_view(), name='user_publicProfile'),
    path('viewProfile/<int:pk>/', ViewProfile.as_view(), name='view_profile'),
]
