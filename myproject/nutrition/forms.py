from django import forms
from .models import Food, Meal
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import ModelForm

class AddFoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ['lebensmittel', 'KH', 'Protein', 'Fett']
			


# class MealForm(ModelForm):
#     class Meta:
#         model = Meal
#         fields = ['meal_name','meal_contents', 'serving_size']



# MealFormSet = inlineformset_factory(Food, Meal, form=MealForm,extra=1)