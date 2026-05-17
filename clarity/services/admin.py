from django.contrib import admin
from .models import Invite, Service, SubjectService, Subject

# Register your models here.

admin.site.register(Invite)
admin.site.register(Service)
admin.site.register(SubjectService)
admin.site.register(Subject)