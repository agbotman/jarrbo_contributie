# Generated by Django 3.1.4 on 2021-06-24 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0036_auto_20210624_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='kortingopdatum',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
