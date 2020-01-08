from django.core.mail import send_mail

from Jalas import settings


def sned_email_arrange_meeting(user, title, link, participants):
    if user.configuration.arrange_meeting and participants:
        try:
            send_mail(
                subject=title,
                message=link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('Check your network connection')


def send_email_add_option(user, title, link, participants):
    if user.configuration.add_option and participants:
        try:
            send_mail(
                subject=title,
                message='Some option added to this poll: \n' + link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('Check your network connection')


def send_email_add_participant(user, title, link, participants):
    if user.configuration.add_new_participant and participants:
        try:
            send_mail(
                subject=title,
                message='You added added to this poll participants: \n' + link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, Check your network connection')


def send_email_remove_option(user, title, link, participants):
    if user.configuration.remove_option and participants:
        try:
            send_mail(
                subject=title,
                message='Some option removed from this poll: \n' + link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, check your network connection')


def send_email_new_vote(user, title, link, participants):
    if user.configuration.remove_option and participants:
        try:
            send_mail(
                subject=title,
                message='You voted to this poll: \n' + link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, Check your network connection')


def send_email_close_poll(user, title, link, participants):
    if user.configuration.remove_option and participants:
        try:
            send_mail(
                subject=title,
                message='This poll was closed: \n' + link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, Check your network connection')
