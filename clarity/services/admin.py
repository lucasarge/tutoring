from django.contrib import admin
from .models import Invite, Service, SubjectService, Subject, Session, Document, Resource

# Register your models here.

admin.site.register(Invite)
admin.site.register(Service)
admin.site.register(SubjectService)
admin.site.register(Subject)
admin.site.register(Document)
admin.site.register(Resource)
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('get_student','start','duration','cost','completed', 'paid')
    list_filter = ('completed','paid')
    ordering = ('-start',)

    @admin.display(description='Student First Name', ordering='service__student__first_name')
    def get_student(self, obj):
        return str(f"{obj.service.student.first_name} {obj.service.student.last_name}")

