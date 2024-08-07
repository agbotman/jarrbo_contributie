# Generated by Django 3.1.4 on 2021-09-05 09:46

import datetime
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0120_auto_20210903_1521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coronarestitution',
            options={'ordering': ['contribution__member__achternaam', 'contribution__member__tussenvoegsels', 'contribution__member__roepnaam'], 'verbose_name': 'payment', 'verbose_name_plural': 'payments'},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': [datetime.datetime], 'verbose_name': 'notes', 'verbose_name_plural': 'notes'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['seizoen', 'contribution__member__achternaam', 'contribution__member__tussenvoegsels', 'contribution__member__roepnaam', 'paymentdate'], 'verbose_name': 'payment', 'verbose_name_plural': 'payments'},
        ),
    ]
