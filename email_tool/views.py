from django.shortcuts import render, get_object_or_404
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


from email_tool.models import EmailMessage, EmailBatch, Customer


@login_required
def preview_batch(request, batch_token):
    email_batch = get_object_or_404(EmailBatch, pk=batch_token)

    customer = Customer(company="Mock Company", first_name="John", last_name="Smith", email="john@smith.com")

    email_message = email_batch.create_email_message(customer)

    context = {
        "customer": customer,
        "email_message": email_message,
        "unsubscribe_link": "https://www.google.com",
    }
    return render(request, f"email/{email_message.template_file}", context)


def unsubscribe(request, message_token):
    """View for Customer unsubscribe action.

    GET/POST http://<app_host>/email/unsubscribe/<message_token>

    Parameters:
        `message_token`: The UUID PK of the EmailMessage object the user
                         is unsubscribing on behalf of.
    Returns:
        If the EmailMessage object does not actually exist in database
        for the parameter `message_token`, we return 404.

        If EmailMessage does exist:
            GET -> Unsubscribe page is returned.
            POST -> Mark Customer is unsubscribed, forward to confirmed page.
            Anything else -> 404 NotFound
    """
    # Load the EmailMessage object form DB or return BadRequest
    email_message = get_object_or_404(EmailMessage, pk=message_token)

    # Update the unsubscribed property on the EmailMessage and save.
    if request.method == "POST":
        email_message.unsubscribed = True
        email_message.save()
        return HttpResponseRedirect(f"{message_token}/confirmed")

    # Any request type other that POST and GET is forbidden
    elif request.method != "GET":
        return HttpResponseNotFound()

    # The template requires the customer object as context as well as
    # the message token to be sent back in the following up POST request.
    context = {"customer": email_message.customer, "message_token": message_token}
    return render(request, "unsubscribe.html", context)


def unsubscribe_confirmed(request, message_token):
    """Unsubscribe confirmed page.

    GET http://<app_host>/email/unsubscribe/<message_token>/confirmed

    Parameters:
        `message_token`: The UUID PK of the EmailMessage object the user
                         is unsubscribing on behalf of.
    Returns:
        If the EmailMessage object does not actually exist in database
        for the parameter `message_token`, we return 404.

        If EmailMessage does exist:
            GET -> Return unsubscribe confirmation page
            Anything else -> 404 NotFound
    """
    # Load the EmailMessage object form DB or return BadRequest
    email_message = get_object_or_404(EmailMessage, pk=message_token)

    if request.method == "GET":
        # The template requires the customer object as context
        context = {"customer": email_message.customer}
        return render(request, "unsubscribe_confirmed.html", context)

    return HttpResponseNotFound()
