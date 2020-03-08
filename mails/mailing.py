from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from parameters.models import EmailList
from django.conf import settings
from django.template.loader import render_to_string


def mail_to_user_booking(
                            sender_email,
                            sender_name,
                            recipient_first_name,
                            recipient_email,
                            subject,
                            booking_id,
                            booking_status,
                            record_type,):
    if record_type == 'new':
        text_template = get_template('mails/booking_new_user.txt')
        html_template = get_template('mails/booking_new_user.html')
    elif record_type == 'update':
        text_template = get_template('mails/booking_update_user.txt')
        html_template = get_template('mails/booking_update_user.html')

    context = {
        'sender_name': sender_name,
        'recipient_name': recipient_first_name,
        'status': booking_status,
        'booking_id': booking_id,
    }
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    msg = EmailMultiAlternatives(subject, text_content, sender_email, [recipient_email])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def mail_to_admin_booking(sender_email,
                          recipient_name,
                          subject,
                          booking_id,
                          record_type,):

    # get list of email of system admin
    recipient_email = EmailList.objects.values_list(
                'email', flat=True).filter(email_type__email_type='company_email')

    if record_type == 'new':
        text_template = get_template('mails/booking_new_admin.txt')
        html_template = get_template('mails/booking_new_admin.html')
    elif record_type == 'update':
        text_template = get_template('mails/booking_update_admin.txt')
        html_template = get_template('mails/booking_update_admin.html')

    context = {
        'recipient_name': recipient_name,
        'booking_id': booking_id,
    }
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    msg = EmailMultiAlternatives(subject, text_content, sender_email, recipient_email)
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def mail_to_user_activation(subject,
                            recipient_email,
                            message_context,
                            ):

    text_template = get_template('mails/user_activate.txt')
    html_template = get_template('mails/user_activate.html')

    text_content = text_template.render(message_context)
    html_content = html_template.render(message_context)

    str_msg = f'subject={subject}, text_content={text_content} ' \
              f'email_host={settings.EMAIL_HOST_USER} ,' \
              f'recipient_email={recipient_email}'

    print(str_msg)

    msg = EmailMultiAlternatives(subject,
                                 text_content,
                                 settings.EMAIL_HOST_USER,
                                 [recipient_email])

    msg.attach_alternative(html_content, "text/html")
    return msg.send()


