""" Database models """

### Python imports ###

### Django imports ###
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


### Third Party imports ###
from auditlog.registry import auditlog

### User Defined imports ###
from email_tool.models import Customer


class Document(models.Model):
    """ This model is for uploading, downloading and browsing documents. """

    allowed_extensions = [
        "doc",
        "docx",
        "pdf",
        "xlsx",
        "xls",
        "png",
        "jpg",
        "csv",
        "pptx",
        "pbix",
    ]

    # TO DO - this should be moved to another file and imported but wasn't working when I tried for some reason.
    # Created a utils.py file and imported from there but this class wasn't recognizing it.
    def validate_max_file_size(value):
        """ Checks that the uploaded file does not exceed the file size limit and returns an error if it does."""
        limit = 25 * 1024 * 1024
        if value.size > limit:
            raise ValidationError("File is too large. Size should not exceed 25 MB.")

    description = models.CharField(max_length=512, help_text="A short description of the file.")
    customer = models.ForeignKey(
        Customer,
        verbose_name="Associated with Customer",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="The customer this document is associated with if there is one.",
    )
    resource = models.FileField(
        upload_to="documents/",
        max_length=100,
        verbose_name="Document",
        help_text=f"Accepted file types: {','.join(allowed_extensions)}.\n Max file size: 25 MB.",
        validators=[
            validate_max_file_size,
            FileExtensionValidator(allowed_extensions=allowed_extensions),
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Upload Document"
        verbose_name_plural = "Upload Documents"

    def __str__(self):
        """ Returns a string representation of the Document object. """
        return f"Document: {self.resource.name}"

    @property
    def file_type(self):
        """ Returns the document file type. """
        for ext in Document.allowed_extensions:
            if self.resource.name.endswith(ext):
                return ext.upper()
        return ""

    # To Do use self.resource.path instead of hardcoding the path.

    @property
    def file_name(self):
        """ Returns the resource file name in a pretty way without the file path or file type."""
        if self.resource is None or self.resource.name is None:
            return ""
        return self.resource.name.split("/")[-1].replace("_", " ")

    @property
    def clean_name(self):
        return self.file_name.replace(self.file_type, "")

    @property
    def file_size(self):
        """ Returns the document file size in megabytes. """
        return self.resource.size


auditlog.register(Document)
