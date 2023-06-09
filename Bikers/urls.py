"""
URL configuration for Bikers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

admin.AdminSite.site_title = 'All1Zed Bikers'
admin.AdminSite.site_header = 'All1Zed Bikers System'
admin.AdminSite.index_title = "Welcome To All1Zed Bikers System"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/packages', views.PackageList.as_view()),
    path('api/packages/<tracking_number>', views.PackageDetail.as_view()),
    path('api/packages/location/update', views.PackagesUpdateLocation.as_view()),
    path('api/courier-companies', views.CourierCompanyList.as_view()),
    path('api/courier-companies/<int:id>',
         views.CourierCompanyDetail.as_view()),
    path('api/bikes', views.MotorBikeList.as_view()),
    path('api/total-sales', views.TotalSales.as_view()),
    path('api/total-sales/<int:vehicle_id>', views.TotalSales.as_view()),
    path('api/total-sales-count', views.TotalSalesCount.as_view()),
    path('api/total-sales-count/<int:vehicle_id>',
         views.TotalSalesCount.as_view()),
    path('api/sort', views.Sorting.as_view()),
]
