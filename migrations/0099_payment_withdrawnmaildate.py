# Generated by Django 3.1.4 on 2021-07-29 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0098_auto_20210729_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='withdrawnmaildate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
