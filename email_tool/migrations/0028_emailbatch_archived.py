# Generated by Django 3.0.7 on 2021-03-21 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("email_tool", "0027_customer_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailbatch",
            name="archived",
            field=models.BooleanField(
                default=False,
                help_text="If checked, this Email Batch will be archived and hidden from the default list view.",
            ),
        ),
    ]
