# Generated by Django 3.0.1 on 2020-01-07 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_delete_comment'),
        ('comment', '0002_auto_20200107_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='poll',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='poll.Poll'),
        ),
    ]
