# Generated by Django 2.2.7 on 2019-11-30 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jalas_back', '0007_auto_20191130_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='room',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='شماره اتاق'),
        ),
    ]
