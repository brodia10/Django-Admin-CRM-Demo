# Generated by Django 3.0.7 on 2020-06-19 00:36

import ckeditor.fields
from django.db import migrations, models
import multiselectfield.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(blank=True, max_length=200, null=True)),
                ("first_name", models.CharField(blank=True, max_length=200)),
                ("last_name", models.CharField(blank=True, max_length=200)),
                ("email", models.EmailField(max_length=254)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
                ),
                (
                    "steel_viking_skills",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ONE", "1"),
                            ("TWO", "2"),
                            ("THREE", "3"),
                            ("FOUR", "4"),
                            ("FIVE", "5"),
                        ],
                        default="THREE",
                        help_text="Rate the Candidates Steel Viking skills.",
                        max_length=256,
                        null=True,
                    ),
                ),
                (
                    "it_skills",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ONE", "1"),
                            ("TWO", "2"),
                            ("THREE", "3"),
                            ("FOUR", "4"),
                            ("FIVE", "5"),
                        ],
                        default="THREE",
                        help_text="Rate the Candidates IT skills.",
                        max_length=256,
                        null=True,
                    ),
                ),
                (
                    "project",
                    models.CharField(
                        blank=True,
                        help_text="Enter what project this Candidate would be hired for.",
                        max_length=200,
                    ),
                ),
                (
                    "tech_stack",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("SQL", "SQL"),
                            ("Java", "Java"),
                            ("Python", "Python"),
                            ("Microsoft PowerBI", "Microsoft PowerBI"),
                            ("MSSQL", "MSSQL"),
                            ("HTML", "HTML"),
                            ("CSS", "CSS"),
                            ("AWS", "AWS"),
                            ("Crystal Reports", "Crystal Reports"),
                        ],
                        help_text="Check the technologies the Candidate has experience with.",
                        max_length=68,
                    ),
                ),
                (
                    "notes",
                    ckeditor.fields.RichTextField(
                        blank=True,
                        help_text="Add any notes about the Candidate",
                        null=True,
                    ),
                ),
            ],
        ),
    ]
