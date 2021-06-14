from collections import defaultdict

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

from datetime import timedelta, date
from decouple import config
from mail_templated import send_mail


from email_tool.models import NextActionItem


class Command(BaseCommand):
    """A emails a report containing all assigned next actions with target date upcoming grouped by assignee.

    Frequency: Once a week

    SCHEDULE THIS TO RUN WEEKLY!!
    """

    help = "Send email notify to `Customer.primary_contact` 7 days or 1 day before `Customer.target_date`"

    def handle(self, *args, **options):

        email_sender = config("EMAIL_USER", "")
        if email_sender == "":
            raise MissingFidelisUserSettings("The app setting 'EMAIL_USER' is missing from the .env file!")

        employees = User.objects.all()

        # Next action with target dates less than 7 days out (includes past due)
        future_threshold = timezone.now() + timedelta(days=7)  # Every report will contain uncompleted from last week
        completed_threshold = timezone.now() - timedelta(
            days=7
        )  # Every report will contain last weeks completed items
        next_action_items = (
            NextActionItem.objects.filter(target_date__lte=future_threshold, assignee__isnull=False)
            .exclude(completed__isnull=False, completed__lte=completed_threshold)
            .order_by("target_date")
            .all()
        )

        # Group the actions by their assignee
        actions_by_user_id = {emp.id: [] for emp in employees}
        employees_by_id = {e.id: e for e in employees}
        for item in next_action_items:
            actions_by_user_id.setdefault(item.assignee.id, []).append(item)

        # This is list of tuples in form [(User, [Customers]), ...]
        assignees_and_actions = [
            (employees_by_id[user_id], actions) for user_id, actions in actions_by_user_id.items()
        ]

        # .. Send email to `employees` containing entire "assignee to actions" report.
        # TODO: Maybe allow users (aka employees) to opt out of this report, filtering HERE.
        recipients = employees
        for recipient in recipients:

            success = self._send_report(
                user=recipient,
                assignees_and_actions=assignees_and_actions,
                sender=f"Fidelis OppDashboard <{email_sender}>",
            )
            if success:
                self.stdout.write(
                    "[" + self.style.SUCCESS("Success") + "] " f"Next action report sent to {recipient.email}"
                )
            else:
                self.stdout.write(
                    "[" + self.style.ERROR("Failed") + "] " f"Next action report didn't send to {recipient.email}"
                )

    def _send_report(self, user, assignees_and_actions, sender):
        now = date.today()
        seven_days_out = now + timedelta(days=7)

        try:
            context = {
                "user": user,
                "assignees_and_actions": assignees_and_actions,
                "now": now,
                "seven_days_out": seven_days_out,
            }

            return 1 == send_mail("email/next_action_report.html", context, sender, [user.email])
        except Exception as e:
            print("\nEXCEPTION:", str(e), "\n")
            return False


class MissingFidelisUserSettings(Exception):
    pass
