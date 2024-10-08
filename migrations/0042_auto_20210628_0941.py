# Generated by Django 3.1.4 on 2021-06-28 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarrbo_contributie', '0041_auto_20210628_0909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='longcategory',
            options={'ordering': ['leeftijdscategory'], 'verbose_name': 'extended category name', 'verbose_name_plural': 'extended category names'},
        ),
        migrations.AlterField(
            model_name='leeftijdscategory',
            name='maximum_age',
            field=models.PositiveIntegerField(default=100, verbose_name='maximum age end of season'),
        ),
    ]
