# Generated by Django 3.0.4 on 2020-04-23 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0005_auto_20200423_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meal',
            old_name='meal_contents',
            new_name='meal_ingredients',
        ),
    ]
