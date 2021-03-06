# Generated by Django 2.2.7 on 2019-12-02 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jalas_back', '0010_auto_20191202_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservationStartTime', models.TimeField(blank=True, default=None, null=True, verbose_name='زمان شروع')),
                ('reservationEndTime', models.TimeField(blank=True, default=None, null=True, verbose_name='زمان پایان')),
                ('meeting', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserveDuration', to='jalas_back.Meeting')),
            ],
        ),
    ]
