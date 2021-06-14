# Generated by Django 3.0.7 on 2020-07-19 03:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("email_tool", "0009_auto_20200718_0556"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageResource",
            fields=[
                (
                    "token",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(max_length=512)),
                (
                    "image",
                    models.ImageField(help_text="Select an image file", upload_to="email_images"),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="emailmessage",
            name="company_logo",
            field=models.ForeignKey(
                help_text="Choose a Company Logo",
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="company_logo_emails",
                to="email_tool.ImageResource",
            ),
        ),
        migrations.AlterField(
            model_name="emailmessage",
            name="customer_image",
            field=models.ForeignKey(
                help_text="Choose a Customer Image",
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="customer_image_emails",
                to="email_tool.ImageResource",
            ),
        ),
        migrations.AlterField(
            model_name="emailmessage",
            name="customer_logo",
            field=models.ForeignKey(
                help_text="Choose a Customer Logo",
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="customer_logo_emails",
                to="email_tool.ImageResource",
            ),
        ),
    ]
