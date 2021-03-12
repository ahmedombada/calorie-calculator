# Generated by Django 3.0.4 on 2020-04-20 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calcalc', '0004_auto_20200414_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessgoal',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='username_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
