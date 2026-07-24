from django.contrib import admin
from .models import Invite, Service, SubjectService, Subject, Session, Document, Resource

# Register your models here.

admin.site.register(Invite)
admin.site.register(Service)
admin.site.register(SubjectService)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(Document)
admin.site.register(Resource)
