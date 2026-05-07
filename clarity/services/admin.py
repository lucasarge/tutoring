from django.contrib import admin
from .models import RegisterService, Service

# Register your models here.

admin.site.register(RegisterService)
admin.site.register(Service)