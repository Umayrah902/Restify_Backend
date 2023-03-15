from django.urls import path
from .views import *

app_name = "properties"
urlpatterns = [
    path('', PropertyInfoFetchView.as_view(), name='property_list_view'),
    path('<int:pk>/', PropertyInfoFocusView.as_view(), name='property_detail_view'),
    path('<int:pk>/aux/', PropertyAuxMediaView.as_view(), name='property_detail_auxiliary_view'),
    path('<int:pk>/aux/manage/', PropertyAuxMediaManageView.as_view(), name='property_detail_auxiliary_mgmt_view'),
    path('<int:pk>/prices/', PropertyPricesView.as_view(), name='property_detail_prices_view'),
    path('<int:pk>/prices/manage/', PropertyPricesManageView.as_view(), name='property_detail_prices_mgmt_view'),
    path('create/', PropertyCreateView.as_view(), name='property_detail_view'),
    path('<int:pk>/edit/', PropertyEditView.as_view(), name='property_detail_view'),
    path('<int:pk>/bookings/', PropertyBookingsView.as_view(), name='property_bookings_view'),
    path('<int:pk>/book/', PropertyBookView.as_view(), name='property_book_view'),
    path('<int:pk>/reviews/', PropertyReviewsView.as_view(), name='property_reviews_view'),
    path('<int:pk>/review/', PropertyReviewAddView.as_view(), name='property_review_add_view'),
    path('<int:pk>/reviews/<int:n>/', PropertyReviewThreadView.as_view(), name='property_review_thread_view'),
    path('<int:pk>/reviews/<int:n>/reply/', PropertyCommentReplyView.as_view(), name='property_comment_reply_view')
]
