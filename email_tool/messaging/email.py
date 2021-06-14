from time import sleep


def send_email(email: str):
    print("Sending email...", end=" ", flush=True)

    # Do actually interacting with emailing library

    # email_recipients = []
    # for user in User.objects.all():
    #     email_recipients.append(user.email)

    # subject = "Fidelis Follow Up - We're implementing so many new features and didn't want you to miss out"
    # html_message = render_to_string(
    #     'email_tool/email_template.html', {'context': 'values'})
    # plain_message = strip_tags(html_message)
    # from_email = 'rodgerdick123@gmail.com'
    # mail.send_mail(subject, plain_message, from_email,
    #                email_recipients, html_message=html_message)

    sleep(1)

    print("Sent!")
    return True
