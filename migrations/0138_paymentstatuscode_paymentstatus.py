# Generated by Django 3.1.4 on 2022-08-02 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0137_auto_20220802_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentstatuscode',
            name='paymentstatus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='jarrbo_contributie.paymentstatus'),
        ),
    ]
