# Generated by Django 3.1.4 on 2021-08-04 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0102_auto_20210804_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='status_code',
        ),
    ]
