# Generated by Django 3.1.4 on 2021-07-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0081_contribution_sponsored'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='inschrijvingsdatum',
            field=models.DateField(null=True),
        ),
    ]
