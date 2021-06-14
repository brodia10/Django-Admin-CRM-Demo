# Generated by Django 3.0.7 on 2021-03-31 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0008_auto_20210225_2235"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="notes",
            field=models.TextField(
                blank=True, help_text="Add any notes about this Candidate.", max_length=1600, null=True
            ),
        ),
    ]
