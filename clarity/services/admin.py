"""This is an admin file that is used to register the database models on the admin dashboard."""

from django.contrib import admin
from .models import Invite, Service, SubjectService, Subject, Session, Document, Resource

# Registering database models for Service to the admin dashboard.
admin.site.register(Invite)
admin.site.register(Service)
admin.site.register(SubjectService)
admin.site.register(Subject)
admin.site.register(Document)
admin.site.register(Resource)

# Allows for filtering option and displays the objects in a more efficient way to use.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('get_student','start','duration','cost','completed', 'paid')
    list_filter = ('completed','paid')
    ordering = ('-start',)

    @admin.display(description='Student First Name', ordering='service__student__first_name')
    def get_student(self, obj):
        return str(f"{obj.service.student.first_name} {obj.service.student.last_name}")

