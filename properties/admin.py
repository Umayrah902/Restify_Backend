from django.contrib import admin
from .models import Property
from .models import Image_Properties
from .models import Date_Price_Properties

admin.site.register(Property)
admin.site.register(Image_Properties)
admin.site.register(Date_Price_Properties)
