# Generated by Django 3.0.4 on 2020-04-27 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0018_auto_20200425_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='meal_contents',
        ),
        migrations.AddField(
            model_name='meal',
            name='meal_contents',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='nutrition.Food'),
        ),
    ]
