from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, GuestSerializer, GuestReviewsSerializer
from rest_framework.permissions import IsAuthenticated
from bookings.models import Booking
from .models import CustomUser
from django.contrib.contenttypes.models import ContentType
from reviews.models import Comment
from django.db.models import Q


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class UserEditProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_object(self):
#         return self.request.user


#see all the users who have reservations/bookings on your property
class ViewGuestsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestSerializer
    def get(self, request):
        #This gives us all the bookings with properties that you own
        bookings = Booking.objects.filter(property_booking__owner=request.user)
        user_set = set()
        for booking in bookings:
            user_set.add(booking.client)
        if user_set:
            user_list = list(user_set)
            return Response(self.serializer_class(user_list, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have no guests'}, status=status.HTTP_400_BAD_REQUEST)

#see the reviews of your guests
class GuestsReviewsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestReviewsSerializer
    def get(self, request, pk):
        
        bookings = Booking.objects.filter(property_booking__owner=request.user)
        user_ids = set()
        for booking in bookings:
            user_ids.add(booking.client.id)
        if pk in user_ids:
            user_ct = ContentType.objects.get_for_model(CustomUser)
            comments = Comment.objects.filter(Q(comment_type=user_ct, comment_id=pk))
            return Response(self.serializer_class(comments, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This user has not reserved any of your properties'}, status=status.HTTP_404_NOT_FOUND)

#you can post a review
class GuestPostReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestReviewsSerializer
    def post(self, request, pk):
        bookings = Booking.objects.filter(property_booking__owner=request.user)
        user_ids = set()
        for booking in bookings:
            user_ids.add(booking.client.id)

        if pk in user_ids:
            try:
                user_ct = ContentType.objects.get_for_model(CustomUser)
                existing_comment = Comment.objects.filter(reviewer=request.user, comment_type=user_ct, comment_id=pk).exists()
                client = CustomUser.objects.get(id=pk)
                booking_status = Booking.objects.filter(client=client, property_booking__owner=request.user, state__in=['Completed']).exists()
                if not existing_comment and booking_status:
                    rating_num = request.data['rating_num']
                    comment_text = request.data['comment_text']
                    reviewer = request.user
                    comment_type = user_ct
                    comment_id = pk
                    user_review = Comment.objects.create(rating_num=rating_num,
                                                comment_text=comment_text,
                                                reviewer=reviewer,
                                                comment_type=comment_type,
                                                comment_id=comment_id)
                    return Response(self.serializer_class(user_review).data, status=status.HTTP_200_OK)
                else:
                    return Response("You cannot comment: You either commented on this user already, or the user has not completed his/her reservation", 
                    status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response("Missing Fields in Request", status=status.HTTP_400_BAD_REQUEST)  

        else:
            return Response({'error': 'This user has not reserved any of your properties'}, status=status.HTTP_404_NOT_FOUND)

