from django.core.mail import send_mail


def booking_notification_email(p_subject, email_info, cal):

    to_email = email_info['user'][0].email
    to_username = email_info['user'][0].username
    booking_id = email_info['booking_id']
    status = email_info['status']

    if cal == 'new':
        mail_message = f'Your booking id {booking_id} is now in "{status}" status and in process by admin.\n\n' \
                       f'We will contact you for confirmation at soonest. \n\n'
    else:
        mail_message = f'Your booking id {booking_id} is updated to "{status}" status.\n\n'

    message = f'Hi {to_username} \n\n' \
              f'{mail_message} \n' \
              f'Thanks for booking with us.\n' \
              f'\n\n' \
              f'Regards\n' \
              f'Admin - Sweep The Floor'
    send_mail(p_subject,    # email subject
              message,      # email body message
              'Sweep The Floor Cleaning Services',  # email from description
              [to_email],  # list of email
              fail_silently=False)
