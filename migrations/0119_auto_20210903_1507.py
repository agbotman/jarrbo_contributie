# Generated by Django 3.1.4 on 2021-09-03 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0118_auto_20210901_0943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coronarestitution',
            old_name='applicable',
            new_name='applied',
        ),
        migrations.AddField(
            model_name='coronarestitution',
            name='s_2021',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coronarestitution',
            name='s_2022',
            field=models.BooleanField(default=False),
        ),
    ]