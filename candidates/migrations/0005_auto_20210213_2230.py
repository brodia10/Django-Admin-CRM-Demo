# Generated by Django 3.0.7 on 2021-02-14 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0004_remove_candidate_follow_up_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="TechStack",
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
                ("name", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name": "Tech stack",
                "verbose_name_plural": "Tech stack",
            },
        ),
        migrations.AlterModelOptions(
            name="candidate",
            options={"verbose_name": "Candidate", "verbose_name_plural": "Candidates"},
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="company",
        ),
        migrations.AddField(
            model_name="candidate",
            name="current_company",
            field=models.CharField(
                blank=True,
                help_text="This is the current company the Candidate is employed at.",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="cv",
            field=models.FileField(
                blank=True,
                default=" ",
                help_text="Upload the Candidate's resume.",
                null=True,
                upload_to="candidate_resumes",
                verbose_name="Resume",
            ),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="it_skills",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ONE", "1"),
                    ("TWO", "2"),
                    ("THREE", "3"),
                    ("FOUR", "4"),
                    ("FIVE", "5"),
                ],
                default="THREE",
                help_text="Rate the Candidates IT and Steel Viking skills.",
                max_length=256,
                null=True,
                verbose_name="IT skills",
            ),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="notes",
            field=models.TextField(
                blank=True,
                help_text="Add any notes about this Candidate.",
                max_length=1000,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="project",
            field=models.CharField(
                blank=True,
                help_text="Enter what project this Candidate would be hired for.",
                max_length=200,
                verbose_name="For Fidelis Project",
            ),
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="tech_stack",
        ),
        migrations.AddField(
            model_name="candidate",
            name="tech_stack",
            field=models.ManyToManyField(
                blank=True,
                help_text="The technologies the Candidate is familiar with. Choose from the list or add a new one from the Tech Stack table.",
                null=True,
                to="candidates.TechStack",
            ),
        ),
    ]
