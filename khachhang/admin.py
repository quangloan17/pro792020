from django.contrib import admin
from .models import * 

admin.site.register(Customer)
admin.site.register(Receipt)
admin.site.register(Order)