# Generated by Django 2.2.7 on 2019-12-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jalas_back', '0008_meeting_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='isCancel',
            field=models.BooleanField(blank=True, default=False, verbose_name='وضعیت لغو'),
        ),
    ]