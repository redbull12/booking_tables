"""BookingRestuarant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from booking.views import api_root, TableViewSet, TableListView, BookingView, ConfirmBookingView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tables', TableViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    # path('api/v1', include('booking.urls')),
    path('api/v1/tables/', TableListView.as_view(), name='tables-list'),
    path('api/v1/booking/', BookingView.as_view()),
    path('confirmation/', ConfirmBookingView.as_view()),
    path('', api_root),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
