# Python imports #

# Django imports #
from django.contrib import admin

# Third Party imports #
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# User-defined imports #
from .models import Candidate, TechStack


class TechStackAdminModel(admin.ModelAdmin):

    fields = ("name",)
    ordering = ("name",)


class CandidateResource(resources.ModelResource):
    """ Used for django-import-export library."""

    class Meta:
        model = Candidate


class CandidateAdminModel(ImportExportModelAdmin):
    """ Used for django-import-export library. """

    resource_class = CandidateResource

    filter_horizontal = ("tech_stack",)
    ordering = ("first_name",)

    fieldsets = [
        (
            "Primary Info",
            {
                "fields": [
                    "primary_contact",
                    "first_name",
                    "last_name",
                    "current_company",
                    "project",
                ]
            },
        ),
        ("Skills", {"fields": ["steel_viking_skills", "it_skills", "tech_stack"]}),
        ("References", {"fields": ["cv", "notes"]}),
    ]

    list_display = [
        "primary_contact",
        "first_name",
        "last_name",
        "current_company",
        "project",
        "steel_viking_skills",
        "it_skills",
        "cv",
        "notes",
    ]

    search_fields = [
        "first_name",
        "tech_stack",
    ]

    # Register your models here.


admin.site.register(Candidate, CandidateAdminModel)
admin.site.register(TechStack, TechStackAdminModel)
