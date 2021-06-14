from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from decouple import config
from mail_templated import send_mail


from email_tool.models import NextActionItem


class Command(BaseCommand):
    """This command will send an email to the assignee of each NextActionItem with
    a target date tomorrow. If two NextActionItems target the same date, two emails
    will be sent.

    SCHEDULE THIS TO RUN DAILY!
    """

    help = "Send email notify to `NextActionItem.assignee` 1 day before `NextActionItem.target_date`"

    def handle(self, *args, **options):

        email_sender = config("EMAIL_USER", "")
        if email_sender == "":
            raise MissingFidelisUserSettings("The app setting 'EMAIL_USER' is missing from the .env file!")

        tomorrow = (timezone.now() + timedelta(days=1)).date()
        next_action_items = NextActionItem.objects.exclude(completed__isnull=False).filter(target_date=tomorrow).all()

        for action in next_action_items:
            success = self._send_action_reminder(
                user=action.assignee,
                action=action,
                sender=f"Fidelis OppDashboard <{email_sender}>",
            )
            if success:
                self.stdout.write(
                    "[" + self.style.SUCCESS("Success") + "] " f"Next action reminder sent to {action.assignee.email}"
                )
            else:
                self.stdout.write(
                    "[" + self.style.ERROR("Failed") + "] "
                    f"Next action reminder didn't send to {action.assignee.email}"
                )

    def _send_action_reminder(self, user, action: NextActionItem, sender):
        context = {
            "seven_days_ahead": False,
            "user": user,
            "target_date": action.target_date,
            "action_item": action.description,
            "relationship_type": action.customer.relationship_type,
            "company": action.customer.company,
            "customer_business_type": action.customer.business_type,
            "customer_service_category": action.customer.service_category,
            "customer_first_name": action.customer.first_name,
            "customer_last_name": action.customer.last_name,
            "customer_role": action.customer.role,
            "customer_email": action.customer.email,
        }

        return 1 == send_mail("email/next_action_reminder.html", context, sender, [user.email])


class MissingFidelisUserSettings(Exception):
    pass
