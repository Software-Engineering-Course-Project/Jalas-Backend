# Generated by Django 2.2.7 on 2019-12-10 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jalas_back', '0013_auto_20191202_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingparticipant',
            name='meeting',
        ),
        migrations.RemoveField(
            model_name='meetingparticipant',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='meeting',
        ),
        migrations.RemoveField(
            model_name='reservationtime',
            name='meeting',
        ),
        migrations.RemoveField(
            model_name='select',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='selectuser',
            name='select',
        ),
        migrations.RemoveField(
            model_name='selectuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='Meeting',
        ),
        migrations.DeleteModel(
            name='MeetingParticipant',
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
        migrations.DeleteModel(
            name='ReservationTime',
        ),
        migrations.DeleteModel(
            name='Select',
        ),
        migrations.DeleteModel(
            name='SelectUser',
        ),
    ]
