# Generated by Django 3.0.7 on 2021-02-14 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("email_tool", "0020_auto_20210207_1803"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="assignee",
            field=models.ForeignKey(
                blank=True,
                help_text="The person assigned to complete the Next Action Item.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="contact_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NOT_SET", "Not Set"),
                    ("BAD_NUMBER", "Bad Number"),
                    ("VOICEMAIL", "Voicemail"),
                    ("SETUP_CALLBACK", "Setup Callback"),
                    ("WARM", "Warm"),
                    ("HOT", "Hot"),
                ],
                default="NOT_SET",
                help_text="This is the status from the last sales call.",
                max_length=256,
                null=True,
                verbose_name="Phone contact status",
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="primary_contact",
            field=models.ForeignKey(
                blank=True,
                help_text="The Customer's primary contact at Fidelis.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_contact",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="secondary_contact",
            field=models.ForeignKey(
                blank=True,
                help_text="The Customer's secondary contact at Fidelis.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="secondary_contact",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="source",
            field=models.CharField(
                blank=True,
                help_text="This is the source of the lead.",
                max_length=200,
                null=True,
            ),
        ),
    ]
