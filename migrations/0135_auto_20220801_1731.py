# Generated by Django 3.1.4 on 2022-08-01 15:31

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0134_auto_20220725_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReversalErrorCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_code', models.CharField(max_length=4, unique=True)),
                ('description', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'errorcode reversal',
                'verbose_name_plural': 'errorcode reversals',
            },
        ),
        migrations.AlterModelManagers(
            name='contribution',
            managers=[
                ('seizoen_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='contributiontable',
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='payment',
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='paymentbatch',
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
