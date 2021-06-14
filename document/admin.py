### Python imports ####

### Django imports ###
from django.contrib import admin
from django.utils.safestring import mark_safe

### Third Party imports ###
from decouple import config

### User-defined imports ###
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            "File",
            {
                "fields": [
                    "description",
                    "resource",
                    "pretty_size",
                    "file_type",
                    "uploaded_at",
                ]
            },
        ),
        (
            "Internal & External",
            {
                "fields": [
                    "customer",
                ]
            },
        ),
    ]

    ordering = ("resource",)

    list_display = [
        "description",
        "link",
        "file_type",
        "pretty_size",
        "customer",
        "uploaded_at",
    ]

    list_filter = ["customer"]

    readonly_fields = ["uploaded_at", "pretty_size", "file_type"]

    def link(self, obj):
        """ Returns a link to the Document, displaying only the filename. """
        media_url = config("AWS_S3_CUSTOM_DOMAIN", "")
        if media_url != "":
            media_url = f"https://{media_url}"

        return mark_safe(f"<a href='{media_url}{obj.resource.url}' target='_blank'>{obj.clean_name}</a>")

    link.short_description = "Link to Document"

    def pretty_size(self, obj):
        """ Returns the size of the document resource. """
        return sizeof_fmt(obj.file_size)

    pretty_size.short_description = "File size"


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)
