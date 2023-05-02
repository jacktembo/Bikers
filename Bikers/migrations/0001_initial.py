# Generated by Django 4.2 on 2023-05-02 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CourierCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=50)),
                (
                    "company_logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="logos",
                        verbose_name="Upload Company logo.",
                    ),
                ),
                ("company_phone_number", models.CharField(max_length=50)),
                ("company_email", models.EmailField(max_length=64)),
                ("address", models.CharField(max_length=100)),
                (
                    "all1zed_commission",
                    models.FloatField(
                        default=5.0,
                        help_text="Commission charged per Package Sent (In Zambian Kwacha)",
                    ),
                ),
                (
                    "number_of_packages",
                    models.IntegerField(
                        default=0, help_text="Initial number of packages."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Login Username",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Courier Companies",
            },
        ),
        migrations.CreateModel(
            name="MotorBike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vehicle_full_name", models.CharField(max_length=255)),
                ("departure_time", models.TimeField()),
                (
                    "transit_time",
                    models.IntegerField(
                        help_text="Number of hours it takes for vehicle to reach the destination."
                    ),
                ),
                (
                    "courier_company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Bikers.couriercompany",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Vehicles",
            },
        ),
        migrations.CreateModel(
            name="PackageInsurance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("percentage", models.FloatField(default=0.0)),
            ],
            options={
                "verbose_name_plural": "Package Insurance",
            },
        ),
        migrations.CreateModel(
            name="PricingPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tier_name",
                    models.CharField(
                        help_text="Pricing Plan Tier Name e.g Gold Standard Plan.",
                        max_length=255,
                    ),
                ),
                ("number_of_packages", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default="..", max_length=100, null=True
                    ),
                ),
                ("session_uuid", models.CharField(max_length=255)),
                ("date_time_created", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("successful", "successful"), ("failed", "failed")],
                        max_length=50,
                    ),
                ),
                ("product_id", models.IntegerField()),
                ("amount", models.FloatField()),
                ("phone_number", models.CharField(max_length=15)),
                (
                    "type",
                    models.CharField(
                        choices=[("cash_in", "cash_in"), ("payment", "payment")],
                        max_length=255,
                    ),
                ),
                (
                    "request_reference",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("provider_reference", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="PendingPaymentApproval",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_uuid", models.CharField(max_length=255)),
                ("product_id", models.CharField(max_length=255)),
                ("date_time_created", models.DateTimeField(auto_now_add=True)),
                ("phone_number", models.CharField(max_length=255)),
                ("reference_number", models.CharField(max_length=255)),
                ("amount", models.FloatField()),
                ("plan_id", models.IntegerField()),
                (
                    "courier_company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Bikers.couriercompany",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tracking_number", models.CharField(editable=False, max_length=255)),
                (
                    "package_value",
                    models.IntegerField(blank=True, default=0.0, null=True),
                ),
                (
                    "processed_by",
                    models.CharField(
                        default="Not Applicable for this package", max_length=255
                    ),
                ),
                ("receiver_name", models.CharField(max_length=255)),
                ("receiver_phone_number", models.CharField(max_length=255)),
                (
                    "sender_name",
                    models.CharField(
                        default="Not Applicable to this package", max_length=255
                    ),
                ),
                ("volume", models.FloatField(blank=True, default=0.0, null=True)),
                ("on_board", models.BooleanField(blank=True, null=True)),
                ("sender_phone_number", models.CharField(max_length=255)),
                ("delivery_town", models.CharField(max_length=255)),
                ("starting_town", models.CharField(default="Lusaka", max_length=255)),
                ("number_of_packages", models.IntegerField(default=1)),
                ("price", models.FloatField(default=0.0)),
                ("departure_date", models.DateField(blank=True, null=True)),
                ("departure_time", models.TimeField()),
                ("processed_date_time", models.DateTimeField(auto_now_add=True)),
                ("transit_date_time", models.DateTimeField(blank=True, null=True)),
                (
                    "ready_for_collection_date_time",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("collected_date_time", models.DateTimeField(blank=True, null=True)),
                (
                    "processed_status",
                    models.BooleanField(blank=True, default=True, null=True),
                ),
                (
                    "transit_status",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "transit_message",
                    models.CharField(default="In transit.", max_length=255),
                ),
                (
                    "ready_for_collection_status",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "collected_status",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "current_coordinates",
                    models.CharField(default="0.0, 0.0", max_length=255),
                ),
                ("previous_town", models.CharField(default="...", max_length=255)),
                (
                    "starting_town_coordinates",
                    models.CharField(default="0.0, 0.0", max_length=255),
                ),
                (
                    "delivery_town_coordinates",
                    models.CharField(default="0.0, 0.0", max_length=255),
                ),
                ("insurance", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "ticket_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Bikers.motorbike",
                    ),
                ),
            ],
        ),
    ]
