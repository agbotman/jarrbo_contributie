# Generated by Django 3.1.4 on 2021-07-11 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0072_auto_20210711_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentstatuschange',
            name='statusafter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statusafter', to='jarrbo_contributie.paymentstatus'),
        ),
        migrations.AlterField(
            model_name='paymentstatuschange',
            name='statusbefore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statusbefore', to='jarrbo_contributie.paymentstatus'),
        ),
    ]
