# Generated by Django 2.2.7 on 2019-12-11 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20191211_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingparticipant',
            name='participant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='participateIn', to=settings.AUTH_USER_MODEL),
        ),
    ]
