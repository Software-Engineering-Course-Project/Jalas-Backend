from django.core.mail import send_mail

from Jalas import settings


def send_email_create_poll(user, title, link, participants):
    if user.configuration.create_poll and participants:
        try:
            send_mail(
                subject=title,
                message=link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants + [user.email]
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


def send_email_add_participant(user, title, link, participants, add):
    if user.configuration.add_new_participant and participants:
        if add:
            mess = 'You added to this poll participants \n' + link
        else:
            mess = 'You removed from this poll participants \n' + link
        try:
            send_mail(
                subject=title,
                message=mess,
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


def send_email_new_vote(user, poll, to):
    if user.configuration.new_vote:
        try:
            send_mail(
                subject=poll.title,
                message='Your voted successfully',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email, poll.meeting.owner.email]
            )
        except:
            print('There are some problem. Plz, Check your network connection')


def send_email_close_poll(user, poll, meetPars):
    if user.configuration.close_poll:
        participants = []
        for meetPar in meetPars:
            par = meetPar.participant
            participants.append(par.email)
        try:
            send_mail(
                subject=poll.title,
                message='This poll was closed. \n',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, Check your network connection')


def send_email_cancel_meeting(user, meeting, meetPars):
    if user.configuration.close_meeting:
        participants = []
        for meetPar in meetPars:
            par = meetPar.participant
            participants.append(par.email)
        try:
            send_mail(
                subject=meeting.title,
                message='This Meeting was canceled. \n',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participants
            )
        except:
            print('There are some problem. Plz, Check your network connection')
