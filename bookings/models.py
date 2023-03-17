from django.db import models
from users.models import CustomUser
from properties.models import Property
from properties.models import AddressField
from django.core.exceptions import ValidationError


class ContactInfo(models.Field):
    def __init__(self, *args, **kwargs):
        self.first_name = models.CharField(max_length=120,null=False, blank=False)
        self.last_name = models.CharField(max_length=120,null=False, blank=False)
        self.email = models.EmailField()
        self.phone_number = models.CharField(max_length=20)
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(255)'
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        first_name, last_name, email, phone_number = value.split(',')
        return {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number}

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return {'first_name': '', 'last_name': '', 'email': '', 'phone_number': ''}
        first_name, last_name, email, phone_number = value.split(',')
        return {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number}

    def get_prep_value(self, value):
        return f"{value['first_name']},{value['last_name']},{value['email']}, {value['phone_number']}"
    
def validate_state(value):
    if value not in dict(Booking.STATES_OPTIONS):
        raise ValidationError('Invalid state')


class Booking(models.Model):
    # allowing client to be null in the case that property is not null 
    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='client')
    # allowing property to be null in the case that client is not null 
    property_booking = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name='property_book')
    # billing_address = AddressField()
    # contact_info = ContactInfo()
    billing_address_string = models.CharField(max_length=255, null=False, blank=False)
    billing_address_city = models.CharField(max_length=255, null=False, blank=False)
    billing_address_country = models.CharField(max_length=255, null=False, blank=False)
    billing_address_province = models.CharField(max_length=255, null=True, blank=True)
    billing_address_postal_code = models.CharField(max_length=10, null=True, blank=True)
    # contact_info_first_name = models.CharField(max_length=120, null=False, blank=False)
    # contact_info_last_name = models.CharField(max_length=120, null=False, blank=False)
    # contact_info_email = models.EmailField()
    # ccontact_info_phone_number = models.CharField(max_length=20)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    invoice_cost = models.IntegerField(null=False, blank=False)
    STATES_OPTIONS = [
        ('Pending', 'Pending'),
        ('Denied', 'Denied'),
        ('Expired', 'Expired'),
        ('Approved', 'Approved'),
        ('RequestCancel', 'RequestCancel'),
        ('Cancelled', 'Cancelled'),
        ('Terminated', 'Terminated'),
        ('Completed', 'Completed'),
    ]
    state = models.CharField(max_length=50, choices=STATES_OPTIONS, default='Pending', validators=[validate_state])
    
