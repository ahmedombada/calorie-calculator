from django.contrib import admin
from .models import FitnessGoal, Workout
# Register your models here.


# @admin.register(FitnessGoal)
# class FitnessGoalAdmin(admin.ModelAdmin, ExportCsvMixin):
# 	...
# 	exclude = ['added_by',]
admin.site.register(FitnessGoal)
admin.site.register(Workout)
exclude = ('added_by',)