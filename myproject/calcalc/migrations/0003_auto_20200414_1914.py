# Generated by Django 3.0.4 on 2020-04-14 17:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calcalc', '0002_auto_20200414_1904'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Calculator',
            new_name='FitnessGoal',
        ),
    ]
