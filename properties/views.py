from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters as rest_filters
from django_filters import rest_framework as filters
from .serializer import PropertySerializer, ImagesSerializer, PriceSerializer, ReviewSerializer, PropertyReplySerializer
from bookings.serializer import BookingSerializer
from bookings.models import Booking
from notifications.models import notifications
from .serializer import PropertySerializer, ImagesSerializer, PriceSerializer
from .models import Property, Image_Properties, Date_Price_Properties
from reviews.models import Comment
from bookings.models import Booking
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class PropertyPagination(PageNumberPagination):
    page_size = 9

class BookingPagination(PageNumberPagination):
    page_size = 15

class PropertyInfoFetchView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    # queryset = Property.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter, rest_filters.SearchFilter ]
    filterset_fields = ['address_city', 'address_province', 'address_country', 'name', 'guest_num', 'amenities', 'owner' ]
    search_fields = ['$address_city', '$address_country', '$name', '$description', ]
    order_fields = ['current_price', 'guest_num']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Property.objects.all()
        queryfrom = self.request.query_params.get('from')
        queryto = self.request.query_params.get('to')

        # print(queryset)

        if queryfrom and queryto:
            conflicts = queryset.filter(property_book__end_date__gt=queryfrom, property_book__start_date__lt=queryto)
            queryset = queryset.exclude(id__in=conflicts)

        return queryset

class PropertyInfoFocusView(APIView):
    def get(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten:
                serializer = PropertySerializer(property_gotten)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

class PropertyAuxMediaView(APIView):
    def get(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten:
                aux_medias = Image_Properties.objects.filter(property=property_gotten)
                # print(aux_medias)
                if aux_medias:
                    imgserializer = ImagesSerializer(aux_medias, many=True)
                    return Response(imgserializer.data, status=HTTP_200_OK)
                else:
                    return Response(status=HTTP_404_NOT_FOUND)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)
class PropertyAuxMediaManageView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                file = request.data['image']
                obj = Image_Properties.objects.create(image=file, property=property_gotten)
                srlz = ImagesSerializer(obj)
                return Response(srlz.data, status=HTTP_201_CREATED)
            except KeyError:
                return Response(status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                pkdeleted = request.headers.get('to-delete')
                img = Image_Properties.objects.get(pk=pkdeleted)
                if img.property != property_gotten:
                    return Response(status=HTTP_401_UNAUTHORIZED)
                img.delete()
                return Response(status=HTTP_200_OK)
            except KeyError:
                return Response(status=HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

class PropertyPricesView(APIView):

    def get(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten:
                prices = Date_Price_Properties.objects.filter(property=property_gotten)
                if prices:
                    priceserializer = PriceSerializer(prices, many=True)
                    return Response(priceserializer.data, status=HTTP_200_OK)
                else:
                    return Response(status=HTTP_404_NOT_FOUND)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

class PropertyPricesManageView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                start_date = request.data['start_date']
                end_date = request.data['end_date']
                price = request.data['pricing']
                conflictings = Date_Price_Properties.objects.filter(end_date__gt=start_date, start_date__lt=end_date).count()
                # if conflictings > 0:
                    # return Response("Conflicting Schedule", status=HTTP_409_CONFLICT)

                obj = Date_Price_Properties.objects.create(start_date=start_date,
                                                end_date=end_date,
                                                pricing=price,
                                                property=property_gotten
                                                )

                srlz = PriceSerializer(obj)
                return Response(srlz.data, status=HTTP_201_CREATED)
            except KeyError:
                return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                pkdeleted = request.headers.get('to-delete')
                pricing = Date_Price_Properties.objects.get(pk=pkdeleted)
                if pricing.property != property_gotten:
                    return Response(status=HTTP_401_UNAUTHORIZED)
                pricing.delete()
                return Response(status=HTTP_200_OK)
            except KeyError:
                return Response(status=HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

class PropertyCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            property_name = request.data['name']
            address_string = request.data['address_string']
            address_city = request.data['address_city']
            address_country = request.data['address_country']
            address_province = request.data['address_province']
            address_postal_code = request.data['address_postal_code']
            guest_num = request.data['guest_num']
            amenities = request.data['amenities']
            description = request.data['description']
            thumbnail_img = request.data['thumbnail_img']
            owner = request.user
            obj = Property.objects.create(
                name=property_name,
                address_string=address_string,
                address_city=address_city,
                address_country=address_country,
                address_province=address_province,
                address_postal_code=address_postal_code,
                guest_num=guest_num,
                amenities=amenities,
                description=description,
                thumbnail_img=thumbnail_img,
                owner=owner
            )

            serializer = PropertySerializer(obj)

            return Response(serializer.data, status=HTTP_201_CREATED)
        except KeyError:
            return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)


class PropertyEditView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                property_gotten.owner = request.user
                property_gotten.property_name = request.data['name']
                property_gotten.address_string = request.data['address_string']
                property_gotten.address_city = request.data['address_city']
                property_gotten.address_country = request.data['address_country']
                property_gotten.address_province = request.data['address_province']
                property_gotten.address_postal_code = request.data['address_postal_code']
                property_gotten.guest_num = request.data['guest_num']
                property_gotten.amenities = request.data['amenities']
                property_gotten.description = request.data['description']
                property_gotten.thumbnail_img = request.data['thumbnail_img']
                property_gotten.save()

                serializer = PropertySerializer(property_gotten)

                return Response(serializer.data, status=HTTP_200_OK)
            except KeyError:
                return Response("Missing Fields in Form.", status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten is None:
                return Response(status=HTTP_404_NOT_FOUND)
            # print(property_gotten)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                if property_gotten.owner != request.user:
                    return Response(status=HTTP_401_UNAUTHORIZED)
                property_gotten.delete()

                return Response(status=HTTP_200_OK)
            except KeyError:
                return Response(status=HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)


class PropertyBookingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten is None:
                return Response(status=HTTP_404_NOT_FOUND)
            if request.user.pk != property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                booking = Booking.objects.filter(property_booking=property_gotten)
                serializer = BookingSerializer(booking, many=True)
                return Response(serializer.data, status=HTTP_200_OK)
            except Exception:
                return Response("Malformed Request", status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)


class PropertyBookView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten is None:
                return Response(status=HTTP_404_NOT_FOUND)
            # Forbid Owners from booking its own property
            if request.user.pk == property_gotten.owner.pk:
                return Response(status=HTTP_403_FORBIDDEN)
            try:
                start_date = request.data['start_date']
                end_date = request.data['end_date']
                billing_address_string = request.data['billing_address_string']
                billing_address_city = request.data['billing_address_city']
                billing_address_country = request.data['billing_address_country']
                billing_address_province = request.data['billing_address_province']
                billing_address_postal_code = request.data['billing_address_postal_code']
                invoice_cost = request.data['invoice_cost']
                state = request.data['state']
                #print(start_date)
                #print(end_date)
                #conflictings = Booking.objects.filter(Q(end_date__gt=start_date) | Q(start_date__lt=end_date)).count()
                #print(conflictings)
                #print(Booking.objects.filter(Q(end_date__gt=start_date) | Q(start_date__lt=end_date)))
                #if conflictings > 0:
                    #return Response("Conflicting Schedule", status=HTTP_409_CONFLICT)

                obj = Booking.objects.create(start_date=start_date,
                                             end_date=end_date,
                                             property_booking=property_gotten,
                                             client=self.request.user,
                                             billing_address_string=billing_address_string,
                                             billing_address_city=billing_address_city,
                                             billing_address_country=billing_address_country,
                                             billing_address_province=billing_address_province,
                                             billing_address_postal_code=billing_address_postal_code,
                                             invoice_cost=invoice_cost,
                                             state=state
                                            )

                booking_ct = ContentType.objects.get_for_model(Booking)

                user_notif = notifications.objects.create(
                    recipient=request.user,
                    details=f"Booking Submitted for Property: {property_gotten.name}, Pending Review.",
                    notification_type=booking_ct,
                    notification_id=obj.pk
                )

                owner_notif = notifications.objects.create(
                    recipient=property_gotten.owner,
                    details=f"Somebody Booked Your Property: {property_gotten.name}.",
                    notification_type=booking_ct,
                    notification_id=obj.pk
                )

                serializer = BookingSerializer(obj)
                # return Response(srlz.data, status=HTTP_201_CREATED)
                return Response(serializer.data, status=HTTP_201_CREATED)
            except KeyError:
                return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)

    """
    def post(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten is None:
            return Response(status=HTTP_404_NOT_FOUND)
    """

    def delete(self, request, pk):
        try:
            property_gotten = Property.objects.get(pk=pk)
            if property_gotten is None:
                return Response(status=HTTP_404_NOT_FOUND)
            # print(property_gotten)
            try:
                if property_gotten.owner != request.user:
                    return Response(status=HTTP_401_UNAUTHORIZED)
                booking_pk = request.headers.get('to-delete')
                booking = Booking.objects.get(pk=booking_pk)
                if booking is None:
                    return Response(status=HTTP_404_NOT_FOUND)
                if booking.property_booking.owner != request.user:
                    return Response(status=HTTP_401_UNAUTHORIZED)
                booking.delete()
                booking_ct = ContentType.objects.get_for_model(Booking)
                user_notif = notifications.objects.create(
                    recipient=booking.client,
                    details=f"The host has cancelled your booking for the property: {property_gotten.name}.",
                    notification_type=booking_ct,
                    notification_id=booking_pk
                )

                return Response(status=HTTP_200_OK)
            except KeyError:
                return Response(status=HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)


class PropertyReviewsView(APIView):
    def get(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            property_ct = ContentType.objects.get_for_model(Property)
            comments = Comment.objects.filter(Q(comment_type=property_ct, comment_id=pk))

            paginator = PageNumberPagination()
            paginator.page_size = 5
            paginated_comments = paginator.paginate_queryset(comments, request)

            serializer = ReviewSerializer(paginated_comments, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

#this is for a non-followup review/comment
class PropertyReviewAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            try:
                #we need to check if this user has commented before on this property or if they are property owner
                #we also need to check if they completed or terminated reservation on this property before
                type_of_object = ContentType.objects.get_for_model(Property)
                existing_comment = Comment.objects.filter(reviewer=request.user, comment_type=type_of_object, comment_id=pk).exists()
                booking_status = Booking.objects.filter(client=request.user, property_booking=property_gotten, state__in=['Terminated', 'Completed']).exists()
                if not existing_comment and booking_status and property_gotten.owner != request.user:
                    rating_num = request.data['rating_num']
                    comment_text = request.data['comment_text']
                    reviewer = request.user
                    comment_type = type_of_object
                    comment_id = pk
                    property_review = Comment.objects.create(rating_num=rating_num,
                                            comment_text=comment_text,
                                            reviewer=reviewer,
                                            comment_type=comment_type,
                                            comment_id=comment_id)
                    serializer = ReviewSerializer(property_review)
                    return Response(serializer.data, status=HTTP_200_OK)
                else:
                    return Response("You cannot comment: You either already commented on this property, have not terminated or completed this property, or are the property owner", 
                    status=HTTP_400_BAD_REQUEST)
                
            except KeyError:
                return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_404_NOT_FOUND)


#view for follow-up messages
class PropertyReviewThreadView(APIView):
    serializer_class = PropertyReplySerializer
    def get(self, request, pk, n):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            property_ct = ContentType.objects.get_for_model(Property)
            property_reviews = Comment.objects.filter(Q(comment_type=property_ct, comment_id=pk))
            comment_id_set = set()
            for reviews in property_reviews:
                comment_id_set.add(reviews.id)
            if n in comment_id_set:
                review_object = Comment.objects.get(id=n)
                owner_reply = review_object.owner_reply
                your_reply = review_object.your_reply
                replies = []
                if owner_reply:
                    replies.append(owner_reply)
                if your_reply:
                    replies.append(your_reply)  
                return Response(self.serializer_class(replies, many=True).data)
            else:
                return Response({'error': 'Invalid notification index'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

#reply to the comments
class PropertyCommentReplyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertyReplySerializer
    def post(self, request, pk, n):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            try:
                property_ct = ContentType.objects.get_for_model(Property)
                property_reviews = Comment.objects.filter(Q(comment_type=property_ct, comment_id=pk))
                comment_id_set = set()
                for reviews in property_reviews:
                    comment_id_set.add(reviews.id)
                if n in comment_id_set:
                    review_object = Comment.objects.get(id=n)
                    owner_reply = review_object.owner_reply
                    your_reply = review_object.your_reply
                    replies = []
                    if not owner_reply and not your_reply and request.user == property_gotten.owner:
                        comment_ct = ContentType.objects.get_for_model(Comment)
                        comment_text = request.data['comment_text']
                        reviewer = request.user
                        comment_type = comment_ct
                        comment_id = review_object.id
                        property_review = Comment.objects.create(
                                                comment_text=comment_text,
                                                reviewer=reviewer,
                                                comment_type=comment_type,
                                                comment_id=comment_id)
                        
                        review_object.owner_reply = property_review
                        review_object.save()
                        replies.append(property_review)
                    elif owner_reply and not your_reply and request.user != property_gotten.owner and review_object.reviewer == request.user:
                        comment_ct = ContentType.objects.get_for_model(Comment)
                        comment_text = request.data['comment_text']
                        reviewer = request.user
                        comment_type = comment_ct
                        comment_id = review_object.id
                        property_review = Comment.objects.create(
                                                comment_text=comment_text,
                                                reviewer=reviewer,
                                                comment_type=comment_type,
                                                comment_id=comment_id)
                        review_object.your_reply = property_review
                        review_object.save()
                        replies.append(property_review)
                    else:
                        return Response({'error': 'You cannot reply'}, status=status.HTTP_400_BAD_REQUEST)

                    return Response(self.serializer_class(replies, many=True).data)
                else:
                    return Response({'error': 'Invalid notification index'}, status=status.HTTP_404_NOT_FOUND)

            except KeyError:
                return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)

        else:
            return Response(status=HTTP_404_NOT_FOUND)


