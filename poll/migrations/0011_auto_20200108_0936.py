# Generated by Django 3.0.1 on 2020-01-08 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_auto_20200107_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='date_close',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ'),
        ),
        migrations.AddField(
            model_name='poll',
            name='status',
            field=models.IntegerField(choices=[(1, 'open'), (2, 'canceled')], default=1, verbose_name='وضعیت رای\u200cگیری'),
        ),
    ]
