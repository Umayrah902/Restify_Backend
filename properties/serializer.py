from .models import Property, Image_Properties, Date_Price_Properties
from reviews.models import Comment
from rest_framework import serializers


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('pk', 'name', 'address_string', 'address_city', 'address_country', 'address_province',
                  'address_postal_code', 'guest_num', 'amenities', 'description', 'thumbnail_img', 'owner',)

    def create(self, validated_data):
        property = Property(**validated_data)
        return property

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image_Properties
        fields = ('pk', 'image',)

    def create(self, validated_data):
        property = ImagesSerializer(**validated_data)
        return property

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Date_Price_Properties
        fields = ('pk', 'start_date','end_date','pricing','property',)

    def create(self, validated_data):
        property = ImagesSerializer(**validated_data)
        return property

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id','rating_num', 'comment_text', 'reviewer')
    
    def create(self, validated_data):
        review = Comment(**validated_data)
        return review

#serializer for the replies to comments
class PropertyReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_text', 'reviewer')
    
    def create(self, validated_data):
        review = Comment(**validated_data)
        return review
