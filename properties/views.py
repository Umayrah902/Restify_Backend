from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters as rest_filters
from django_filters import rest_framework as filters
from .serializer import PropertySerializer, ImagesSerializer, PriceSerializer, ReviewSerializer
from .models import Property, Image_Properties, Date_Price_Properties
from reviews.models import Comment
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class PropertyInfoFetchView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter, rest_filters.SearchFilter, ]
    filterset_fields = ['address_city', 'address_province', 'address_country', 'name', 'guest_num', ]
    search_fields = ['$address', '$name', '$description', ]
    order_fields = ['current_price', 'guest_num']

class PropertyInfoFocusView(APIView):
    def get(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            serializer = PropertySerializer(property_gotten)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

class PropertyAuxMediaView(APIView):
    def get(self, request, pk):
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

class PropertyAuxMediaManageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
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

    def delete(self, request, pk):
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

class PropertyPricesView(APIView):
    def get(self, request, pk):
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

class PropertyPricesManageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if request.user.pk != property_gotten.owner.pk:
            return Response(status=HTTP_403_FORBIDDEN)
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            price = request.data['pricing']
            conflictings = Date_Price_Properties.objects.filter(Q(end_date__gt=start_date) |
                                                                    Q(start_date__lt=end_date)).count()
            if conflictings > 0:
                return Response("Conflicting Schedule", status=HTTP_409_CONFLICT)

            obj = Date_Price_Properties.objects.create(start_date=start_date,
                                            end_date=end_date,
                                            pricing=price,
                                            property=property_gotten
                                            )

            srlz = PriceSerializer(obj)
            return Response(srlz.data, status=HTTP_201_CREATED)
        except KeyError:
            return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
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
            return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        print(property_gotten)
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


class PropertyBookingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        return None

class PropertyBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        return None


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

class PropertyReviewAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        property_gotten = Property.objects.get(pk=pk)
        if property_gotten:
            #create a comment object, check if that user has posted a non follow up comment yet
            #if they have not, (0 comments) and they completed/terminated reservation, then they
            #are allowed to comment, else raise an HTTP error
            
            pass
        else:
            return Response(status=HTTP_404_NOT_FOUND)

        return None
