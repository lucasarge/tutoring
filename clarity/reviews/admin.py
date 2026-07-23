from django.contrib import admin
from .models import Review, ReviewCategory, Category

# Register your models here.
admin.site.register(Review)
admin.site.register(ReviewCategory)
admin.site.register(Category)