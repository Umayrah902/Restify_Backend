from django.db import models
# note: you need to 'pip install django-multiselectfield' 
from multiselectfield import MultiSelectField
from users.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime

class AddressField(models.Field):
    def __init__(self, *args, **kwargs):
        self.address_line_one = models.CharField(max_length=255, null=False, blank=False)
        self.city = models.CharField(max_length=255, null=False, blank=False)
        self.country = models.CharField(max_length=255, null=False, blank=False)
        self.province = models.CharField(max_length=255, null=True, blank=True)
        self.postal_code = models.CharField(max_length=10, null=True, blank=True)
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(255)'
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        address_line_one, city, country, province, postal_code = value.split(',')
        return {'address_line_one': address_line_one, 'city': city, 'country': country, 'province': province, 'postal_code': postal_code}

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return {'address_line_one': '', 'city': '', 'country': '', 'province': '', 'postal_code': ''}
        address_line_one, city, country, province, postal_code = value.split(',')
        return {'address_line_one': address_line_one, 'city': city, 'country': country, 'province': province, 'postal_code': postal_code}

    def get_prep_value(self, value):
        return f"{value['address_line_one']},{value['city']},{value['country']}, {value['province']}, {value['postal_code']}"

def validate_min_choices(value):
    if len(value) < 0:
        raise ValidationError('You cannot have a negative number of choices.')

class Property(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    # address = AddressField()
    address_string = models.CharField(max_length=255, null=False, blank=False)
    address_city = models.CharField(max_length=255, null=False, blank=False)
    address_country = models.CharField(max_length=255, null=False, blank=False)
    address_province = models.CharField(max_length=255, null=True, blank=True)
    address_postal_code = models.CharField(max_length=10, null=True, blank=True)
    guest_num = models.IntegerField(null=False, blank=True)
    AMENITIES_CHOICES = (
    ('Wifi', 'Wifi'),
    ('Kitchen', 'Kitchen'),
    ('Parking', 'Parking'),
    ('TV', 'TV'),
    ('Toiletries', 'Toiletries'),
    ('Workspace', 'Workspace'),
    ('Self-CheckIn', 'Self-CheckIn'),
    ('Free Cancellation Within 24 hours', 'Free Cancellation Within 24 hours'),
    ('Free Cancellation Within 48 hours', 'Free Cancellation Within 48 hours'),
    ('Free Cancellation Within one week', 'Free Cancellation Within one week'),
    )
    amenities = MultiSelectField(choices=AMENITIES_CHOICES)
    description = models.TextField(max_length=500, null=False, blank=False)
    thumbnail_img = models.ImageField(upload_to='properties_thumbnails/', null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='owner')

    @property
    def current_price(self):
        if self.dates_prices.all():
            return self.dates_prices.filter(start_date__gte=datetime.today(), end_date__lt=datetime.today())[0].pricing
        return 0


    @property
    def image_gallery(self):
        if self.images.all():
            return self.images.all()

# model to create images for the properties - a property can have multiple images
class Image_Properties(models.Model):
    image = models.ImageField(upload_to='properties_images/',null=False, blank=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='images')

# model to create pricing for different date ranges
class Date_Price_Properties(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    pricing = models.FloatField(null=False, blank=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='dates_prices')

    # the same property have different pricing for the same start and end date together
    class Meta:
        unique_together = ('start_date', 'end_date', 'property')