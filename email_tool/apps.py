from django.apps import AppConfig


class EmailToolConfig(AppConfig):
    name = "email_tool"
    label = "email_tool"
    verbose_name = "Email Tool"

    def ready(self):
        # Importing the signal handlers here is standard practice.
        import email_tool.signal_handlers  # noqa
