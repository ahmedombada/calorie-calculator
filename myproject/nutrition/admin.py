from django.contrib import admin
from .models import Food, Meal
# from .models import Meal
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Food, Meal)
class Food(ImportExportModelAdmin):
	pass 
		
class MealInline(admin.StackedInline):
    model = Meal

class FoodAdmin(admin.ModelAdmin):
    inlines = [
        MealInline,
    ]