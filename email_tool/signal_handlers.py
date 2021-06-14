""" Module containing Django Signals handler functions. """
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from mail_templated import send_mail
from email_tool.models import EmailMessage
from decouple import config

DEFAULT_EMAIL_SENDER = config("EMAIL_USER", "")


@receiver(post_save, sender=EmailMessage)
def execute_email_send(sender, instance, created, **kwargs):
    """Called anytime an EmailMessage instance is saved to the db,
    including newly created instances and updates.

    For newly created EmailMessage objects, this callback actually sends
    the email to the customer containing the template specified in the
    EmailMessage model.

    This then updates that EmailMessage instance to show if the send
    completed successfully.
    """
    if created:  # Only if this is a new instance to the database
        # Actually sends an email after the `EmailMessage` object has
        # been created in the database
        customer = instance.customer

        if not customer.is_dnc():
            instance.custom_message
            unsubscribe_link = f"{settings.UNSUBSCRIBE_ROUTE_BASE}/{instance.token}"
            context = {
                "customer": customer,
                "unsubscribe_link": unsubscribe_link,
                "email_message": instance,
            }
            print(f"Sending email '{instance.template_file}' to '{customer.email}'...")
            result = send_mail(
                f"email/{instance.template_file}",
                context,
                f"Fidelis Partners <{DEFAULT_EMAIL_SENDER}>",
                [customer.email],
                fail_silently=False,
            )

            # Save if the mail was able to send to the EmailMessage instance
            instance.send_succeeded = result == 1

        else:
            instance.send_succeeded = False
            print(f"Customer '{customer.email}' is unsubscribed, NO EMAIL SENT.")

        instance.save()
