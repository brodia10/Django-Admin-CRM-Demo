# Generated by Django 3.0.7 on 2020-10-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("email_tool", "0013_auto_20200817_1927"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="source",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="customer",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
    ]
