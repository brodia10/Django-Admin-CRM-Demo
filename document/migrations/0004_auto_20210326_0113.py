# Generated by Django 3.0.7 on 2021-03-26 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("document", "0003_auto_20210218_0134"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="document",
            options={"verbose_name": "Upload Document", "verbose_name_plural": "Upload Documents"},
        ),
    ]
