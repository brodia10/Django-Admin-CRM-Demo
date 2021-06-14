""" Database models """

### Python imports ###
import uuid
from enum import Enum
from datetime import datetime, timedelta

### Django imports ###
from django.db import models
from django.utils.html import escape, mark_safe, format_html
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django.conf import settings
from django.urls import reverse

### Third Party imports ###
from phone_field import PhoneField
from ckeditor.fields import RichTextField
from auditlog.registry import auditlog
from gsheets import mixins


class ImageCategory(models.TextChoices):
    """Image Category: Internal, Customer, Marketing"""

    INTERNAL = "Internal"
    CUSTOMER = "Customer"
    MARKETING = "Marketing"


class NextActionItemStatus(models.TextChoices):
    """Status choices for Next Action Item."""

    PAST_DUE = "Past Due"
    TO_DO = "To Do"
    COMPLETED = "Completed"


class ServiceCategory(Enum):
    """ Enum for service category the customer is seeking. """

    IT = "IT"
    STEEL_VIKING = "Steel Viking"
    IT_AND_STEEL_VIKING = "It and Steel Viking"
    NOT_SET = "Not set"
    OTHER = "Other"


class ContactStatus(Enum):
    """ Enum for the status of a customer contact. """

    NOT_SET = "Not Set"
    BAD_NUMBER = "Bad Number"
    VOICEMAIL = "Voicemail"
    SETUP_CALLBACK = "Setup Callback"
    WARM = "Warm"
    HOT = "Hot"


class BusinessType(Enum):
    """ Enum for the status of a customer contact. """

    OTHER = "Other"
    MANUFACTURING = "Manufacturing"
    HEALTHCARE = "Healthcare"
    FINANCE = "Finance"


class RelationshipType(Enum):
    """ Enum for the status of a customer contact. """

    CUSTOMER = "Customer"
    PROSPECT = "Prospect"
    PARTNER = "Partner"
    OTHER = "Other"
    NOT_SET = "Not Set"


class InterestLevel(Enum):
    """ Enum for the level of interest of a customer contact. """

    ONE = "1 – No interest, initial prospect, some interest in the past but has cooled"
    TWO = "2 – Promising and ongoing interaction with prospect, meetings happening, possible work identified"
    THREE = "3 – Work identified and statement made that prospect wants to ultimately work with us – path forward"
    FOUR = "4 – Real opportunity for work under consideration, specific work and timeframe identified, Fidelis identified as serious contender"
    FIVE = "5 – Nearing work approval"


class Customer(mixins.SheetPushableMixin, models.Model):
    """ The core of the app. Our customer """

    # Google Sheets API settings
    spreadsheet_id = settings.GSHEETS_CUSTOMER_SHEET_ID
    sheet_id_field = "Customer ID"
    sheet_name = "Customers"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="This is the source of the lead.",
    )
    master_company = models.CharField(max_length=200, verbose_name="Master company", null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254)
    phone = PhoneField(blank=True, help_text="Contact phone number", null=True, max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    last_contacted = models.DateField(
        verbose_name="Last contacted",
        null=True,
        blank=True,
        help_text="This is the last time the Customer was contacted.",
    )
    next_action_item = models.TextField(
        null=True,
        blank=True,
        help_text="This is for solid, defined next actions. Use the Description field for general notes.",
    )
    target_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Target date",
        help_text="This is the Target Date for the Next Action Item. This should only be used if there is a Next Action Item.",
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Assignee",
        related_name="assignee",
        help_text="The person assigned to complete the Next Action Item.",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="This is for general descriptions, notes, or any info you want to add about the contact.",
    )
    relationship_type = models.CharField(
        max_length=256,
        choices=[(relationship.name, relationship.value) for relationship in RelationshipType],
        default=RelationshipType.PROSPECT.name,
        null=True,
        blank=True,
    )
    service_category = models.CharField(
        max_length=256,
        choices=[(service.name, service.value) for service in ServiceCategory],
        default=ServiceCategory.IT.name,
        null=True,
        blank=True,
    )
    interest_level = models.CharField(
        max_length=256,
        choices=[(level.name, level.value) for level in InterestLevel],
        default=InterestLevel.ONE.name,
        null=True,
        blank=True,
    )
    primary_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Primary contact",
        related_name="primary_contact",
        help_text="The Customer's primary contact at Fidelis.",
    )
    secondary_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="secondary_contact",
        help_text="The Customer's secondary contact at Fidelis.",
    )
    contact_status = models.CharField(
        max_length=256,
        choices=[(status.name, status.value) for status in ContactStatus],
        default=ContactStatus.NOT_SET.name,
        null=True,
        blank=True,
        verbose_name="Phone contact status",
        help_text="This is the status from the last sales call.",
    )
    business_type = models.CharField(
        max_length=256,
        choices=[(business.name, business.value) for business in BusinessType],
        default=BusinessType.MANUFACTURING.name,
        null=True,
        blank=True,
    )
    website = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        """ Returns a string representation of all Customer fields for a nicer display. """
        return f"{self.company}"

    def last_emailed_at(self):
        """Queries this customers EmailMessage to find the
        timestamp of the last email we sent.
        """
        sent_emails = EmailMessage.objects.filter(customer=self, send_succeeded=True).order_by("created_at").all()
        if len(sent_emails) > 0:
            return sent_emails[0].created_at
        return None

    def is_dnc(self):
        """Queries this customers EmailMessage to determine if
        they've unsubsubscribe in response to any of them.
        """
        return EmailMessage.objects.filter(customer=self, unsubscribed=True).count() > 0

    @property
    def short_description(self):
        """ Truncates the description field to the specified length. """
        return truncatechars(self.description, 100)


class ImageResource(models.Model):
    """Database record of image resources. Creating a relationship with
    this class will allow for the reusage of the same image resource in
    mass email batches.
    """

    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=512)
    image = models.ImageField(upload_to="email_images", help_text="Select an image file")
    category = models.CharField(choices=ImageCategory.choices, max_length=16, default=ImageCategory.MARKETING.value)
    archived = models.BooleanField(
        default=False,
        help_text="If checked, this Image will be archived and hidden from the default list view.",
    )

    def __str__(self):
        return f"Image file: {self.description}"

    def image_tag(self):
        return mark_safe('<img src="%s" />' % escape(self.image.url))

    image_tag.short_description = "Image"
    image_tag.allow_tags = True


class EmailTemplate(Enum):
    """ Enum mapping available email templates to files. """

    SIMPLE = "simple.html"
    MODERN_STANDARD = "modern_standard.html"


# TODO: return the correct default image url here
DEFAULT_IMAGE_URL = "https://cdn0.iconfinder.com/data/icons/feather/96/no-512.png"


class EmailMessage(models.Model):
    """ Persistence for an email we've sent to customer. """

    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    send_succeeded = models.BooleanField(
        default=False,
        blank=True,
        help_text="Indicates that an email has been sent and whether it succeeded or failed.",
    )
    template_file = models.CharField(
        max_length=256,
        choices=[(templ.value, templ.name) for templ in EmailTemplate],
        default=EmailTemplate.MODERN_STANDARD.value,
    )
    subject = models.CharField(max_length=256, null=True)

    company_logo = models.ForeignKey(
        ImageResource,
        related_name="company_logo_emails",
        on_delete=models.DO_NOTHING,
        help_text="Primary Company logo",
    )
    alt_company_logo = models.ForeignKey(
        ImageResource,
        on_delete=models.DO_NOTHING,
        help_text="If one is not chosen, the above Company Logo will be used.",
        verbose_name="Secondary Company logo",
        null=True,
        blank=True,
    )
    title = RichTextField(null=True, blank=True)
    primary_image = models.ForeignKey(
        ImageResource,
        null=True,
        blank=True,
        related_name="primary_image_emails",
        on_delete=models.DO_NOTHING,
        help_text="The primary marketing image for the email.",
    )

    # ckeditor Rich Text Field
    custom_message = RichTextField(null=True, blank=True)
    call_to_action_button_text = models.CharField(max_length=256, default="Learn More")
    call_to_action_button_link = models.CharField(max_length=256, default="http://www.fidelis-partners.com/")

    # Results filled by customer interaction with email
    unsubscribed = models.BooleanField(default=False, blank=True)

    batch = models.ForeignKey(
        "EmailBatch",
        related_name="email_messages",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return f"Email sent to {self.customer}"

    @property
    def get_company_logo_absolute_url(self):
        if self.company_logo is None:
            return DEFAULT_IMAGE_URL
        return self.company_logo.image.url

    @property
    def get_company_secondary_logo_absolute_url(self):
        """Returns alt_company_logo if there is one, otherwise returns company_logo."""
        if self.alt_company_logo is not None:
            return self.alt_company_logo.image.url
        else:
            return self.company_logo.image.url

    @property
    def get_primary_image_absolute_url(self):
        if self.primary_image is None:
            return DEFAULT_IMAGE_URL
        return self.primary_image.image.url


class EmailBatch(models.Model):
    """Stores the parameters of a mass email batch. This is mostly
    the same as what is on each `EmailMessage` but allows for future
    batches to be sent containing the same form data.
    """

    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    batch_title = models.CharField(
        max_length=50,
    )

    #
    # Parameters of the batch
    #

    template_file = models.CharField(
        max_length=256,
        choices=[(templ.value, templ.name) for templ in EmailTemplate],
        default=EmailTemplate.MODERN_STANDARD.value,
    )

    subject = models.CharField(max_length=256, null=True)
    title = RichTextField(null=True)
    custom_message = RichTextField(null=True)
    call_to_action_button_text = models.CharField(
        max_length=256,
        help_text="This will be the text used for the main Call To Action button in the email. You want to make it something short and attention-grabbing.",
    )
    call_to_action_button_link = models.CharField(
        max_length=256,
        help_text="This will be the link that a user is sent to after clicking the main Call To Action button in the email.",
    )
    company_logo = models.ForeignKey(
        ImageResource,
        related_name="company_logo_batches",
        on_delete=models.DO_NOTHING,
        help_text="Primary company logo.",
    )
    alt_company_logo = models.ForeignKey(
        ImageResource,
        on_delete=models.DO_NOTHING,
        help_text="If one is not chosen, the above Company Logo will be used.",
        verbose_name="Secondary company logo",
        null=True,
        blank=True,
    )
    primary_image = models.ForeignKey(
        ImageResource,
        related_name="primary_image_batches",
        on_delete=models.DO_NOTHING,
        help_text="The primary marketing image for the email.",
    )
    emails_initiated = models.IntegerField(default=0, help_text="The number of emails that were sent in this batch.")
    emails_skipped = models.IntegerField(
        default=0,
        help_text="The number of emails skipped in this batch due to Customers that have unsubscribed.",
    )
    archived = models.BooleanField(
        default=False,
        help_text="If checked, this Email Batch will be archived and hidden from the default list view.",
    )

    def __str__(self):
        return f"Email batch: {self.batch_title}"

    def emails_sent(self):
        """Queries for the number of emails that succeeded to
        send for this batch.
        """
        return EmailMessage.objects.filter(batch=self, send_succeeded=True).count()

    def unsubscribe_count(self):
        """Queries for the number of emails in this batch that customers
        have used to unsubscribe.
        """
        return EmailMessage.objects.filter(batch=self, unsubscribed=True).count()

    def create_email_message(self, customer: Customer):
        """Uses the values stored in this instance to create a new
        EmailMessage object. It has NOT been saved to the DB yet tho,
        so edits may still take place.
        """
        return EmailMessage(
            customer=customer,
            template_file=self.template_file,
            subject=self.subject,
            title=self.title,
            custom_message=self.custom_message,
            call_to_action_button_text=self.call_to_action_button_text,
            call_to_action_button_link=self.call_to_action_button_link,
            company_logo=self.company_logo,
            alt_company_logo=self.alt_company_logo,
            company_logo_id=self.company_logo_id,
            primary_image=self.primary_image,
            primary_image_id=self.primary_image_id,
            batch=self,
        )

    def clone(self, new_batch_title: str):
        """Constructs a new EmailBatch instance with all the same
        field values except for the `batch_title`. It does not get
        saved to the Db.
        """
        return EmailBatch(
            batch_title=new_batch_title,
            template_file=self.template_file,
            subject=self.subject,
            title=self.title,
            custom_message=self.custom_message,
            call_to_action_button_text=self.call_to_action_button_text,
            call_to_action_button_link=self.call_to_action_button_link,
            company_logo=self.company_logo,
            company_logo_id=self.company_logo_id,
            alt_company_logo=self.alt_company_logo,
            primary_image=self.primary_image,
            primary_image_id=self.primary_image_id,
        )

    @property
    def preview_link(self):
        preview_url = reverse("preview_batch", kwargs={"batch_token": self.pk})
        return mark_safe(f'<a href="{preview_url}" target="_blank">Preview<a/>')  # noqa

    class Meta:
        verbose_name = "Email batch"
        verbose_name_plural = "Email batches"


class NextActionItem(models.Model):
    """Model definition for NextActionItem."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer",
        help_text="The Customer this Next Action Item relates to.",
    )
    description = models.TextField(max_length=256, help_text="Describe this Next Action Item.")
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Assignee",
        help_text="The person assigned to complete this Next Action Item.",
    )
    target_date = models.DateField(help_text="The Target Date for this Next Action Item.", verbose_name="Target date")
    completed = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Completed",
        help_text="IMPORTANT: Add the completed time once this Next Action Item is completed.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        """Meta definition for NextActionItem."""

        verbose_name = "Next Action Item"
        verbose_name_plural = "Next Action Items"

    """Method definitions for NextActionItem."""

    def __str__(self):
        """Unicode representation of NextActionItem."""
        return f"Next Action Item: {self.customer} {self.target_date}"

    @property
    def short_description(self):
        """Truncates the description field to the specified length."""
        return truncatechars(self.description, 50)

    @property
    def status(self):
        """ Returns Next Action Item Status: Past Due, Completed, or To Do."""
        if self.completed is not None:
            return mark_safe(
                f'<p style="background: white; color: seagreen; padding:1px; border: solid 1px seagreen; border-radius: 6px; text-align: center;">{NextActionItemStatus.COMPLETED}</p>'
            )  # noqa
        elif self.completed is None and self.target_date < datetime.now().date():
            return mark_safe(
                f'<p style="background: red; color: white; padding:1px; border: solid 1px red; border-radius: 6px; text-align: center;">{NextActionItemStatus.PAST_DUE}</p>'
            )  # noqa
        else:
            return mark_safe(
                f'<p style="background: white; color: dodgerblue; padding:1px; border: solid 1px dodgerblue; border-radius: 6px; text-align: center;">{NextActionItemStatus.TO_DO}</p>'
            )  # noqa

    status.fget.short_description = "Status"


auditlog.register(Customer)
auditlog.register(EmailBatch)
auditlog.register(EmailMessage)
auditlog.register(NextActionItem)
