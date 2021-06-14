### Python Imports ###
from enum import Enum

### Django Imports ###
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

### Third Party Imports ###
from phone_field import PhoneField
from auditlog.registry import auditlog


class SteelVikingSkills(Enum):
    """ Enum for the Steel Viking skills of a potential candidate. """

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class ITSkills(Enum):
    """ Enum for the IT skills of a potential candidate. """

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class TechStack(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tech stack"
        verbose_name_plural = "Tech stack"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Candidate(models.Model):
    """ The core of our app, our Candidates. """

    primary_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The Candidate's primary contact at Fidelis.",
    )
    current_company = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="This is the current company the Candidate is employed at.",
    )
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254)
    phone = PhoneField(blank=True, help_text="Contact phone number", null=True, max_length=50)
    steel_viking_skills = models.CharField(
        max_length=256,
        choices=[(skill.name, skill.value) for skill in SteelVikingSkills],
        default=SteelVikingSkills.THREE.name,
        null=True,
        blank=True,
        help_text="Rate the Candidates Steel Viking skills.",
    )
    it_skills = models.CharField(
        max_length=256,
        choices=[(skill.name, skill.value) for skill in SteelVikingSkills],
        default=ITSkills.THREE.name,
        null=True,
        blank=True,
        verbose_name="IT skills",
        help_text="Rate the Candidates IT skills.",
    )
    project = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="For Fidelis Project",
        help_text="Enter what project this Candidate would be hired for.",
    )
    tech_stack = models.ManyToManyField(
        TechStack,
        blank=True,
        null=True,
        help_text="The technologies the Candidate is familiar with. Choose from the list or add a new one from the Tech Stack table.",
    )
    cv = models.FileField(
        upload_to="candidate_resumes",
        default=" ",
        verbose_name="Resume",
        blank=True,
        null=True,
        help_text="Upload the Candidate's resume.",
    )
    notes = models.TextField(
        max_length=1600,
        null=True,
        blank=True,
        help_text="Add any notes about this Candidate.",
    )

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        """ Returns a string representation of the Candidates first and last name for easy readibility. """
        return f"{self.first_name} {self.last_name}"


auditlog.register(Candidate)
