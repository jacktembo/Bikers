from datetime import datetime, timedelta
import pytz
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import sms, phone_numbers
from .models import *
from .serializers import PackageSerializer, MotorBikeSerializer, CourierCompanySerializer, UserSerializer

today = datetime.today()

utc = pytz.UTC


def index(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'index.html')
        elif request.user.is_authenticated and request.user.is_superuser:
            return redirect('kazang-dashboard')
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('kazang-dashboard')
        else:
            return render(request, 'index.html')


class PackageList(ListCreateAPIView):
    def get_queryset(self):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name
        return Package.objects.filter(vehicle__courier_company__company_name=company_name)

    def get_serializer_class(self):
        return PackageSerializer

    filterset_fields = ['vehicle', 'departure_date', 'processed_by', 'delivery_town', 'starting_town',
                        'collected_status', 'package_value', 'number_of_packages', 'price',
                        'departure_time', 'transit_date_time', 'ready_for_collection_date_time', 'collected_date_time',
                        'ready_for_collection_status', 'on_board']

    def create(self, request, *args, **kwargs):
        sender_phone_number = self.request.data['sender_phone_number']
        receiver_phone_number = self.request.data['receiver_phone_number']
        price = self.request.data['price']
        receiver_name = self.request.data['receiver_name']
        starting_town = self.request.data['starting_town']
        insurance = self.request.data.get('insurance', False)
        description = self.request.data.get('description', None)
        ticket_number = self.request.data.get('ticket_number', None)
        data1 = request.data
        serializer = self.get_serializer(data=data1)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        tracking_number = serializer.data[next(iter(serializer.data))]
        vehicle = MotorBike.objects.get(id=int(serializer.data['vehicle']))
        company = vehicle.courier_company
        if company.number_of_packages > 1:
            company_name = vehicle.courier_company.company_name
            receiver_message = f"Dear {receiver_name}, your package has been received by {company_name} Courier at {starting_town} station and processed " \
                               f"for dispatch. Tracking No. {tracking_number} Courier charge K{price}. Check your package status at https://packages.all1zed.com. "
            sender_message = f"Dear Customer, the package you are sending has been processed " \
                             f"for dispatch. Tracking No. {tracking_number} Courier charge K{price}. Check your package status at https://packages.all1zed.com. "
            sms.send_sms(receiver_phone_number, receiver_message)
            sms.send_sms(sender_phone_number, sender_message)
            headers = self.get_success_headers(serializer.data)
            remaining_packages = vehicle.courier_company.number_of_packages
            company.number_of_packages = remaining_packages - 1
            company.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return 'Insufficient Balance. Please To Up.'


class PackagesUpdateLocation(APIView):
    def post(self, request):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name
        vehicle = MotorBike.objects.get(id=int(self.request.query_params.get('vehicle_id', None)))
        current_coordinates = self.request.data.get('current_coordinates', None)
        packages = Package.objects.filter(vehicle__courier_company__company_name=company_name, vehicle=vehicle)
        packages.update(current_coordinates=current_coordinates)
        return Response({'status': 'successfully updated'}, status=status.HTTP_200_OK)


class PackageDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'tracking_number'

    def get_serializer_class(self):
        return PackageSerializer

    def get_queryset(self):
        if self.request.user.username == 'app':
            return Package.objects.all()
        else:
            group = self.request.user.groups.all().first()
            group_name = group.name
            company = CourierCompany.objects.get(company_name=group_name)
            company_name = company.company_name
            return Package.objects.filter(vehicle__courier_company__company_name=company_name)


class MotorBikeList(ListCreateAPIView):
    def get_queryset(self):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name

        return MotorBike.objects.filter(courier_company__company_name=company_name)

    def get_serializer_class(self):
        return MotorBikeSerializer


class CourierCompanyList(ListCreateAPIView):
    def get_queryset(self):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name

        return CourierCompany.objects.filter(company_name=company_name)

    def get_serializer_class(self):
        return CourierCompanySerializer


class CourierCompanyDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'

    def get_serializer_class(self):
        return CourierCompanySerializer

    def get_queryset(self):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name

        return CourierCompany.objects.filter(company_name=company_name)


class TotalSales(APIView):
    """
    Get total sales for whole company or specified bus.
    """

    def get(self, request):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        if vehicle_id == None:
            result = Package.objects.filter(departure_date=today,
                                            vehicle__courier_company__company_name=company_name).aggregate(
                Sum('price')).get('price__sum')
            return Response(result)
        else:
            group = self.request.user.groups.all().first()
            group_name = group.name
            company = CourierCompany.objects.get(company_name=group_name)
            company_name = company.company_name
            result = Package.objects.filter(departure_date=today, vehicle__courier_company__company_name=company_name,
                                            vehicle__id=int(vehicle_id)).aggregate(Sum('price')).get('price__sum')
            return Response(result)


class TotalSalesCount(APIView):
    def get(self, request):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        if vehicle_id == None:
            result = Package.objects.filter(departure_date=today,
                                            vehicle__courier_company__company_name=company_name).count()
            return Response(result)

        else:
            result = Package.objects.filter(departure_date=today, vehicle__courier_company__company_name=company_name,
                                            vehicle__id=int(vehicle_id)).count()
            return Response(result)


class Sorting(APIView):
    def post(self, request):
        town = request.data.get('town', None)
        tracking_number = request.data.get('tracking_number', None)
        package = Package.objects.filter(tracking_number=tracking_number)
        receiver_phone_number = package.first().receiver_phone_number
        destination_town = package.first().delivery_town
        if town is not None:
            if town.lower() == destination_town.lower():
                package.update(transit_status=False, ready_for_collection_status=True,
                               transit_message=f'ready for collection at {town} town')
                message = f'Dear Customer, your package with Tracking No. {tracking_number} is ready for collection at {town} station. Thank you for choosing {package.first().vehicle.courier_company} courier.'
                sms.send_sms(receiver_phone_number, message)
                return Response(PackageSerializer(package.first()).data, status=status.HTTP_200_OK)
            else:
                package.update(transit_message=f'In Transit, passed through {town} station.')
                return Response(PackageSerializer(package.first()).data, status=status.HTTP_200_OK)
        vehicle_id = request.data.get('vehicle_id', None)
        if vehicle_id is not None:
            tracking_number = request.data.get('tracking_number', None)
            package = Package.objects.filter(tracking_number=tracking_number)
            vehicle = MotorBike.objects.filter(id=int(vehicle_id)).first()
            package.update(vehicle=vehicle)
            return Response(PackageSerializer(package.first()).data)


class CompanyUsersList(ListAPIView):
    def get_queryset(self):
        group = self.request.user.groups.all().first()
        group_name = group.name
        company = CourierCompany.objects.get(company_name=group_name)
        company_name = company.company_name
        return User.objects.filter(groups__in=self.request.user.groups.all())

    def get_serializer_class(self):
        return UserSerializer
