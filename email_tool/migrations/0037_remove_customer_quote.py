# Generated by Django 3.0.7 on 2021-03-30 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("email_tool", "0036_updated_related_name_primary_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="emailbatch",
            name="customer_quote",
        ),
        migrations.RemoveField(
            model_name="emailmessage",
            name="customer_quote",
        ),
    ]
