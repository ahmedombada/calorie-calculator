# Generated by Django 3.1.7 on 2021-03-21 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0029_auto_20200502_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meal',
            old_name='meal_name',
            new_name='meal',
        ),
    ]
