# Generated by Django 3.0.7 on 2021-02-07 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("email_tool", "0019_auto_20210205_1504"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emailbatch",
            options={
                "verbose_name": "Email batch",
                "verbose_name_plural": "Email batches",
            },
        ),
        migrations.AlterField(
            model_name="emailmessage",
            name="customer_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose a Customer Image",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="customer_image_emails",
                to="email_tool.ImageResource",
            ),
        ),
        migrations.AlterField(
            model_name="emailmessage",
            name="customer_logo",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose a Customer Logo",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="customer_logo_emails",
                to="email_tool.ImageResource",
            ),
        ),
    ]
