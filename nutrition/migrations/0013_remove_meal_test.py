# Generated by Django 3.0.4 on 2020-04-23 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0012_meal_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='test',
        ),
    ]