# Generated by Django 3.1.4 on 2021-05-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0003_auto_20210529_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='refresh_all',
            field=models.BooleanField(default=False),
        ),
    ]
