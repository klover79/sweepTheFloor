from django.core.mail import send_mail
from parameters.models import ActivateBoolean, EmailList, EmailType
from .models import Booking


def booking_notification_email(p_subject, email_info, cal):

    to_email = email_info['user'][0].email
    to_username = email_info['user'][0].username
    booking_id = email_info['booking_id']
    status = email_info['status']

    bookings = Booking.objects.filter(id=booking_id)

    send_to_company_email = ActivateBoolean.objects.values_list(
        'activate', flat=True).filter(activation_type='send_to_company_email')

    send_to_user_email = ActivateBoolean.objects.values_list(
        'activate', flat=True).filter(activation_type='send_to_user_email')

    company_email = [tuple(EmailList.objects.values_list(
        'email', flat=True).filter(email_type__email_type='company_email'))]

    if cal == 'new':
        mail_message = f'Your booking id {booking_id} is now in "{status}" status and under process by admin.\n\n' \
                       f'We will contact you for confirmation at soonest. \n\n'
        mail_message_admin = f'A Booking has been raised.\n\n' \
                             f'Please login to SweepTheFloor to contact user and confirm the booking\n\n' \
                             f'Booking ID  : {booking_id}\n' \
                             f'User: {to_username}\n' \
                             f'Email: {to_email}\n'
        message_admin = f'Hi Admin \n\n' \
                        f'{mail_message_admin} \n' \
                        f'Thanks.\n' \
                        f'\n\n' \
                        f'Regards\n' \
                        f'Sweep The Floor'

    else:
        mail_message = f'Your booking id {booking_id} is updated to "{status}" status.\n\n'

    message = f'Hi {to_username} \n\n' \
              f'{mail_message} \n' \
              f'Thanks for booking with us.\n' \
              f'\n\n' \
              f'Regards\n' \
              f'Admin - Sweep The Floor'

    if send_to_user_email[0]:
        send_mail(p_subject,    # email subject
                  message,      # email body message
                  'Sweep The Floor Cleaning Services',  # email from description
                  [to_email],  # list of email
                  fail_silently=False)

    if cal == 'new' and send_to_company_email[0]:
        send_mail(p_subject,  # email subject
                  message_admin,  # email body message
                  'Sweep The Floor Cleaning Services',  # email from description
                  company_email,  # list of email
                  fail_silently=False)

