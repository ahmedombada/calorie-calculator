# Generated by Django 3.0.4 on 2020-04-29 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0022_auto_20200428_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='overall_Calories',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
