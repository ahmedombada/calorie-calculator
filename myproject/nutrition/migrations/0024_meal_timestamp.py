# Generated by Django 3.0.4 on 2020-04-29 17:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0023_auto_20200429_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
