from django.contrib import admin
from .models import *


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):

    def from_town(self, package: Package):
        return package.starting_town

    def status(self, package: Package):
        return "Collected" if package.collected_status else "Not Collected"

    list_display = [
        'tracking_number',  'receiver_name', 'receiver_phone_number',
        'vehicle', 'from_town', 'delivery_town', 'departure_date', 'departure_time',
        'price', 'status',

    ]


@admin.register(CourierCompany)
class CourierCompanyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CourierCompany._meta.fields]


@admin.register(MotorBike)
class MotorBikeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MotorBike._meta.fields]


@admin.register(PackageInsurance)
class PackageInsuranceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PackageInsurance._meta.fields]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields]
