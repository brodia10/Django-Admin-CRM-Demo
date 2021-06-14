### Python imports ####
from datetime import datetime

### Django imports ###
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now

### Third Party imports ###
from ckeditor.widgets import CKEditorWidget
from import_export.admin import ImportExportModelAdmin
from import_export import resources

### User-defined imports ###
from .models import (
    Customer,
    EmailMessage,
    EmailTemplate,
    ContactStatus,
    BusinessType,
    ImageResource,
    EmailBatch,
    ServiceCategory,
    RelationshipType,
    NextActionItem,
    NextActionItemStatus,
    ImageCategory,
)


class ImageCategoryFilter(admin.SimpleListFilter):

    title = "Category"
    parameter_name = "Category"

    def lookups(self, request, model_admin):
        return (
            ("Internal", "Internal"),
            ("Customer", "Customer"),
            ("Marketing", "Marketing"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Internal":
            return queryset.filter(category=ImageCategory.INTERNAL.value)
        elif value == "Customer":
            return queryset.filter(category=ImageCategory.CUSTOMER.value)
        elif value == "Marketing":
            return queryset.filter(category=ImageCategory.MARKETING.value)
        return queryset


class ArchivedFilter(SimpleListFilter):
    """This filter returns unarchived EmailBatches."""

    title = "Status"

    parameter_name = "Archived"

    def lookups(self, request, model_admin):
        return (
            ("Archived", "Archived"),
            ("Active", "Active"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Archived":
            return queryset.filter(archived=True)
        value = "Active"
        return queryset.filter(archived=False)


class NextActionItemStatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "Status"

    def lookups(self, request, model_admin):
        return (
            ("To Do", "To Do"),
            ("Past Due", "Past Due"),
            ("Completed", "Completed"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Completed":
            return queryset.filter(completed__isnull=False)
        elif value == "Past Due":
            return queryset.filter(completed__isnull=True, target_date__lt=datetime.now().date())
        elif value == "To Do":
            return queryset.filter(completed__isnull=True, target_date__gt=datetime.now().date())
        return queryset


class StatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "Status"

    def lookups(self, request, model_admin):
        return (
            ("Bad Number", "Bad Number"),
            ("Voicemail", "Voicemail"),
            ("Setup Callback", "Setup Callback"),
            ("Warm", "Warm"),
            ("Hot", "Hot"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Bad Number":
            return queryset.filter(contact_status=ContactStatus.BAD_NUMBER.name)
        elif value == "Voicemail":
            return queryset.filter(contact_status=ContactStatus.VOICEMAIL.name)
        elif value == "Setup Callback":
            return queryset.filter(contact_status=ContactStatus.SETUP_CALLBACK.name)
        elif value == "Warm":
            return queryset.filter(contact_status=ContactStatus.WARM.name)
        elif value == "HOT":
            return queryset.filter(contact_status=ContactStatus.HOT.name)
        return queryset


class BusinessTypeFilter(admin.SimpleListFilter):
    title = "Business Type"
    parameter_name = "Business Type"

    def lookups(self, request, model_admin):
        return (
            ("Manufacturing", "Manufacturing"),
            ("Finance", "Finance"),
            ("Healthcare", "Healthcare"),
            ("Other", "Other"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Manufacturing":
            return queryset.filter(business_type=BusinessType.MANUFACTURING.name)
        elif value == "Finance":
            return queryset.filter(business_type=BusinessType.FINANCE.name)
        elif value == "Healthcare":
            return queryset.filter(business_type=BusinessType.HEALTHCARE.name)
        elif value == "Other":
            return queryset.filter(business_type=BusinessType.OTHER.name)
        return queryset


class ServiceCategoryFilter(admin.SimpleListFilter):
    title = "Service Category"
    parameter_name = "Service Category"

    def lookups(self, request, model_admin):
        return (
            ("IT", "IT"),
            ("Steel Viking", "Steel Viking"),
            ("Not set", "Not set"),
            ("Other", "Other"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "IT":
            return queryset.filter(service_category=ServiceCategory.IT.name)
        elif value == "Steel Viking":
            return queryset.filter(service_category=ServiceCategory.STEEL_VIKING.name)
        elif value == "Not set":
            return queryset.filter(service_category=ServiceCategory.NOT_SET.name)
        elif value == "Other":
            return queryset.filter(service_category=ServiceCategory.OTHER.name)
        return queryset


class RelationshipTypeFilter(admin.SimpleListFilter):
    title = "Relationship Type"
    parameter_name = "Relationship Type"

    def lookups(self, request, model_admin):
        return (
            ("Customer", "Customer"),
            ("Prospect", "Prospect"),
            ("Partner", "Partner"),
            ("Other", "Other"),
            ("Not set", "Not set"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Customer":
            return queryset.filter(relationship_type=RelationshipType.CUSTOMER.name)
        elif value == "Prospect":
            return queryset.filter(relationship_type=RelationshipType.PROSPECT.name)
        elif value == "Partner":
            return queryset.filter(relationship_type=RelationshipType.PARTNER.name)
        elif value == "Other":
            return queryset.filter(relationship_type=RelationshipType.OTHER.name)
        elif value == "Not set":
            return queryset.filter(relationship_type=RelationshipType.NOT_SET.name)
        return queryset


class ImageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Image: {obj.description} -- {obj.image} ({obj.image.width} x {obj.image.height})"


class EmailBatchChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Batch: {obj.batch_title}"


class CreateNewEmailBatchForm(forms.Form):
    """ The form used by the `Send Mass Email` action. """

    template_file = forms.CharField(
        widget=forms.Select(choices=[(templ.value, templ.name) for templ in EmailTemplate])
    )
    subject = forms.CharField(max_length=254)
    title = forms.CharField(widget=CKEditorWidget())
    custom_content = forms.CharField(widget=CKEditorWidget())
    call_to_action_button_text = forms.CharField(max_length=254, initial="Learn More")
    call_to_action_button_link = forms.CharField(max_length=254, initial="http://www.fidelis-partners.com/")

    company_logo = ImageChoiceField(queryset=ImageResource.objects.all())
    primary_image = ImageChoiceField(queryset=ImageResource.objects.all())
    batch_title = forms.CharField(
        max_length=256,
        required=True,
        help_text="Provide a name for this mass email batch to refer to easily refer to it later.",
    )


class SendExistingEmailBatchForm(forms.Form):
    selected_batch = EmailBatchChoiceField(queryset=EmailBatch.objects.filter(archived=False))
    batch_title = forms.CharField(
        max_length=256,
        required=True,
        help_text="Provide a name for the new email batch.",
    )


@admin.register(NextActionItem)
class NextActionItemAdminModel(admin.ModelAdmin):
    """Admin View for NextActionItem"""

    list_display = [
        "target_date",
        "customer",
        "short_description",
        "assignee",
        "completed",
        "status",
    ]

    list_filter = [
        NextActionItemStatusFilter,
        "customer",
        "assignee",
        "target_date",
        "created_at",
    ]

    readonly = ["created_at"]

    search_fields = (
        "customer",
        "description",
        "assignee",
    )
    ordering = ("-target_date",)

    actions = ["mark_completed"]

    def mark_completed(self, request, queryset):
        queryset.update(completed=now())

    mark_completed.short_description = "Mark selected items completed"


class NextActionItemInline(admin.StackedInline):
    """Next Action Item Inline"""

    model = NextActionItem
    extra = 0
    verbose_name = "Next Action Item"
    fields = [
        "assignee",
        "target_date",
        "description",
        "completed",
    ]


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


@admin.register(Customer)
class CustomerAdminModel(ImportExportModelAdmin):
    """ Used for django-import-export library."""

    resource_class = CustomerResource

    ### List Display, Search, Ordering, Actions and Filters ###

    fieldsets = [
        (
            "Primary Info",
            {"fields": ["company", "first_name", "last_name", "role", "last_contacted", "description"]},
        ),
        (
            "Fidelis Contacts",
            {
                "fields": [
                    "primary_contact",
                    "secondary_contact",
                ]
            },
        ),
        (
            "Relationship",
            {
                "fields": [
                    "relationship_type",
                    "interest_level",
                    "service_category",
                    "business_type",
                ]
            },
        ),
        (
            "Contact Info",
            {
                "fields": [
                    "email",
                    "phone",
                ]
            },
        ),
        (
            "Address",
            {
                "fields": [
                    "address",
                    "city",
                    "state",
                    "zip_code",
                ]
            },
        ),
        (
            "General Info",
            {
                "fields": [
                    "master_company",
                    "source",
                    "website",
                ]
            },
        ),
    ]

    ordering = ("company",)

    inlines = [NextActionItemInline]

    list_display = [
        "company",
        "primary_contact",
        "last_contacted",
        "short_description",
        "service_category",
        "interest_level",
        "business_type",
        "relationship_type",
        "next_actions_pastdue",
    ]

    search_fields = [
        "company",
        "service_category",
        "first_name",
        "last_name",
        "email",
        "city",
        "contact_status",
        "business_type",
        "master_company",
        "relationship_type",
    ]

    list_filter = [
        "primary_contact",
        "assignee",
        "last_contacted",
        ServiceCategoryFilter,
        RelationshipTypeFilter,
        BusinessTypeFilter,
        # IsDncFilter,
        StatusFilter,
        "master_company",
    ]

    actions = [
        "create_new_email_batch",
        "send_existing_batch_to_different_customers",
    ]

    def next_actions_pastdue(self, obj):
        pastdue_count = obj.nextactionitem_set.filter(completed__isnull=True, target_date__lt=now()).count()
        if pastdue_count > 0:
            return mark_safe(f'<b style="background:red; color: white; padding:5px;">{pastdue_count}</b>')  # noqa
        return ""

    next_actions_pastdue.short_description = "Next actions past due"

    def status(self, customer):
        """ Styles the color for each item in the status field"""
        if customer.contact_status in [None, ""]:
            return mark_safe(f'<b style="background: gray; color: white; padding:5px;">No Value</b>')  # noqa

        status = ContactStatus[customer.contact_status]
        color = "white"
        if status == ContactStatus.BAD_NUMBER:
            color = "red"
        elif status == ContactStatus.VOICEMAIL:
            color = "magenta"
        elif status == ContactStatus.SETUP_CALLBACK:
            color = "blue"
        elif status == ContactStatus.WARM:
            color = "orange"
        elif status == ContactStatus.HOT:
            color = "green"
        else:
            color = "gray"

        return mark_safe(f'<b style="background:{color}; color: white; padding:5px;">{status.value}</b>')

    def can_email(self, customer):
        return not customer.is_dnc()

    can_email.boolean = True
    can_email.short_description = "Can Email"

    def last_emailed_at(self, customer):
        return customer.last_emailed_at()

    last_emailed_at.short_description = "Last Emailed"

    def create_new_email_batch(self, request, queryset):
        """Action handler for creating an email batch with full control
        over the values injected into the template.
        """
        # If the 'Preview' submission button was clicked, then
        # we return the email template filled with the form values
        # in a new tab, i.e. a preview.
        if "preview" in request.POST:
            return self._build_preview_for_new_batch(request, queryset)

        # Else if the 'apply' submission button was clicked, actually
        # initiate the mass email.
        elif "apply" in request.POST:
            return self._execute_mass_email(request, queryset)

        # If not a submission request, then we just render the form page
        # for the user to fill out.
        context = {
            "customers": queryset,
            "form": CreateNewEmailBatchForm(),
            "action": "create_new_email_batch",
        }
        return render(request, "admin/mass_email_form.html", context=context)

    create_new_email_batch.short_description = "Create new email batch to selected customers"

    def send_existing_batch_to_different_customers(self, request, queryset):
        """Action handler for sending an email batch that is a clone
        of an existing batch but to new customers.

        NOTE: This creates a complete new EmailBatch instance with the
        same values, but requires a new title to differentiate the clone
        from the original.
        """
        # If the 'Preview' submission button was clicked, then
        # we return the email template filled with the form values
        # in a new tab, i.e. a preview.
        if "preview" in request.POST:
            existing_batch = EmailBatch.objects.get(pk=request.POST["selected_batch"])
            return self._build_preview_for_existing_batch(request, queryset, existing_batch)

        # Else if the 'apply' submission button was clicked, actually
        # initiate the mass email.
        elif "apply" in request.POST:
            existing_batch = EmailBatch.objects.get(pk=request.POST["selected_batch"])
            return self._execute_mass_email(request, queryset, existing_batch)

        # If not a submission request, then we just render the form page for the user to fill out.
        context = {
            "customers": queryset,
            "form": SendExistingEmailBatchForm(),
            "action": "send_existing_batch_to_different_customers",
        }
        return render(request, "admin/mass_email_form.html", context=context)

    send_existing_batch_to_different_customers.short_description = "Send existing email batch to selected customers"

    def _build_preview_for_new_batch(self, request, queryset):
        """Return the rendered email template with the current
        form values rendered, i.e. a "Preview". Make sure the submit
        button uses `formtarget="_blank"` so it opens in a new tab.
        """
        customer = queryset[0]  # we use first customer just for preview
        values = request.POST

        # Creates a tmp instance so we can pass it to the template for rendering
        email_message = EmailMessage()
        email_message.subject = values["subject"]
        email_message.title = values["title"]
        email_message.custom_message = values["custom_content"]
        email_message.call_to_action_button_text = values["call_to_action_button_text"]
        email_message.call_to_action_button_link = values["call_to_action_button_link"]

        if _not_blank(values, "company_logo"):
            email_message.company_logo = ImageResource.objects.get(pk=values["company_logo"])

        if _not_blank(values, "alt_company_logo"):
            email_message.alt_company_logo = ImageResource.objects.get(pk=values["alt_company_logo"])

        if _not_blank(values, "primary_image"):
            email_message.primary_image = ImageResource.objects.get(pk=values["primary_image"])

        template_file = values["template_file"]
        context = {
            "customer": customer,
            "email_message": email_message,
            "unsubscribe_link": "https://www.google.com",
        }
        return render(request, f"email/{template_file}", context)

    def _build_preview_for_existing_batch(self, request, queryset, batch):
        """Return the rendered email template with values from
        the pre-existing selected email batch, i.e. a "Preview".
        Make sure the submit button uses `formtarget="_blank"` so
        it opens in a new tab.
        """
        customer = queryset[0]  # we use first customer just for preview
        email_message = batch.create_email_message(customer)
        template_file = batch.template_file

        context = {
            "customer": customer,
            "email_message": email_message,
            "unsubscribe_link": "https://www.google.com",
        }
        return render(request, f"email/{template_file}", context)

    def _execute_mass_email(self, request, queryset, existing_batch=None):
        """Loop over the customer queryset and send an email to each one.

        Arguments:
            `request`: The Django `Request` object from the admin site we're
                responding to.
            `queryset`: The set of customers the mass email is targeting. This
                is decided by what customers in the customer list were selected
                when initiating the mass email action.
            `existing_batch`: (Optional) If provided, new EmailBatch instance
                is created with the same values as the passed instance, except
                it gets a new title from the `"batch_title"` form value.
                The EmailMessages created are attached to this new batch, not
                the pre-existing one. If not provided or `None`, a new EmailBatch
                instance is created directly from the request's POST values.
        """
        values = request.POST

        if existing_batch is None:
            new_batch = EmailBatch.objects.create(
                batch_title=values["batch_title"],
                template_file=values["template_file"],
                subject=values["subject"],
                title=values["title"],
                custom_message=values["custom_content"],
                call_to_action_button_text=values["call_to_action_button_text"],
                call_to_action_button_link=values["call_to_action_button_link"],
                company_logo_id=_get_or_none(values, "company_logo"),
                alt_company_logo_id=_get_or_none(values, "alt_company_logo"),
                primary_image_id=_get_or_none(values, "primary_image"),
            )
        else:
            new_batch = existing_batch.clone(values["batch_title"])
            new_batch.save()

        # Iterate thru customer queryset and create an EmailMessage for each.
        initiated, skipped = 0, 0
        for customer in queryset.all():

            if customer.is_dnc():
                skipped += 1
                continue

            # We use a factory method on the BatchEmail object we just
            # created to construct the EmailMessage objects then immediately
            # call save(), initiating sending the object via signal handler.
            new_batch.create_email_message(customer).save()
            initiated += 1

        # Update the EmailBatch object with the results of the sending themails
        new_batch.emails_initiated = initiated
        new_batch.emails_skipped = skipped
        new_batch.save()

        self.message_user(
            request,
            f" We reached {initiated} prospects with this email! {skipped} did not receive this email because they have unsubscribed",
        )
        return HttpResponseRedirect(request.get_full_path())


@admin.register(EmailMessage)
class EmailMessageAdminModel(admin.ModelAdmin):

    fieldsets = [
        (
            "Title & Template Options",
            {
                "fields": [
                    "batch",
                    "template_file",
                ]
            },
        ),
        (
            "Email Content",
            {
                "fields": [
                    "subject",
                    "title",
                    "custom_message",
                ]
            },
        ),
        (
            "Call To Action",
            {
                "fields": [
                    "call_to_action_button_text",
                    "call_to_action_button_link",
                ]
            },
        ),
        ("Images", {"fields": ["company_logo", "alt_company_logo", "primary_image"]}),
    ]

    list_display = ["created_at", "customer", "token", "send_succeeded", "batch_id"]
    search_fields = ["customer", "send_succeeded"]
    readonly_fields = ["send_succeeded", "unsubscribed"]

    ordering = ("-created_at",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["company_logo", "alt_company_logo", "primary_image"]:
            return ImageChoiceField(queryset=ImageResource.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ImageResource)
class ImageResourceAdminModel(admin.ModelAdmin):
    list_display = [
        "description",
        "category",
        "resolution",
        "image",
        "uploaded_at",
    ]
    fields = ["description", "category", "archived", "image", "resolution", "image_tag", "full_url"]
    readonly_fields = ["image_tag", "resolution", "full_url"]
    list_filter = [ImageCategoryFilter, ArchivedFilter]
    ordering = ("description",)
    actions = ["archive_action", "unarchive_action"]

    def resolution(self, obj):
        return f"{obj.image.width} x {obj.image.height}"

    def full_url(self, obj):
        return obj.image.url

    def archive_action(modeladmin, request, queryset):
        """This action marks selected Email Batches as archived."""
        queryset.update(archived=True)

    archive_action.short_description = "Archive selected Images"

    def unarchive_action(modeladmin, request, queryset):
        """This action marks selected Images as unarchived."""
        queryset.update(archived=False)

    unarchive_action.short_description = "Unarchive selected Images"


@admin.register(EmailBatch)
class EmailBatchAdminModel(admin.ModelAdmin):

    fieldsets = [
        (
            "Title & Template Options",
            {
                "fields": [
                    "batch_title",
                    "template_file",
                    "archived",
                ]
            },
        ),
        (
            "Email Content",
            {
                "fields": [
                    "subject",
                    "title",
                    "custom_message",
                ]
            },
        ),
        (
            "Call To Action",
            {
                "fields": [
                    "call_to_action_button_text",
                    "call_to_action_button_link",
                ]
            },
        ),
        ("Images", {"fields": ["company_logo", "alt_company_logo", "primary_image"]}),
        (
            "Sent & Skipped",
            {
                "fields": [
                    "emails_initiated",
                    "emails_skipped",
                ]
            },
        ),
    ]

    list_display = [
        "batch_title",
        "template_file",
        "preview_link",
        "emails_sent",
        "emails_skipped",
        "unsubscribe_count",
        "created_at",
    ]
    list_filter = [ArchivedFilter]

    ordering = ("batch_title",)

    def archive_action(modeladmin, request, queryset):
        """This action marks selected Email Batches as archived."""
        queryset.update(archived=True)

    archive_action.short_description = "Archive selected Email Batches"

    def unarchive_action(modeladmin, request, queryset):
        """This action marks selected Email Batches as unarchived."""
        queryset.update(archived=False)

    unarchive_action.short_description = "Unarchive selected Email Batches"

    actions = [archive_action, unarchive_action]


def _not_blank(POST, property_name):
    return POST.get(property_name) not in [None, ""]


def _get_or_none(POST, property_name):
    return POST[property_name] if _not_blank(POST, property_name) else None
