# Generated by Django 3.0.7 on 2021-01-18 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("email_tool", "0015_auto_20210115_1941"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="primary_contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_contact",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="relationship_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CUSTOMER", "Customer"),
                    ("PROSPECT", "Prospect"),
                    ("PARTNER", "Partner"),
                    ("OTHER", "Other"),
                    ("NOT_SET", "Not Set"),
                ],
                default="PROSPECT",
                max_length=256,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="secondary_contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="secondary_contact",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="service_category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("IT", "IT"),
                    ("STEEL_VIKING", "Steel Viking"),
                    ("NOT_SET", "Not set"),
                    ("OTHER", "Other"),
                ],
                default="IT",
                max_length=256,
                null=True,
            ),
        ),
    ]
