# Generated by Django 3.0.1 on 2020-01-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectuser',
            name='agreement',
            field=models.IntegerField(choices=[(1, 'خیر'), (2, 'بله'), (3, 'اگر مجبور بودم می\u200cآیم')], null=True, verbose_name='نظر'),
        ),
    ]
