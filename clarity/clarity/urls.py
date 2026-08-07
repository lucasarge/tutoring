"""This is a urls file that runs different views through a specified path."""

"""
URL configuration for clarity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

# This is the root app of Clarity Tutoring therefore is the hub to connect all the other apps.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('help/', include('help.urls')),
    path('users/', include('users.urls')),
    path('services/', include('services.urls')),
    path('reviews/', include('reviews.urls'))
]

# This defines where the static files are located.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
