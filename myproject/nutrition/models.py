from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.db.models import F

# the meal database colomns consist of (lebensmittel,carbohydrates per 100 g, fett, protein, calories) its all pro 100 grams and its float type
# Create your models here.


class Food(models.Model):
	lebensmittel = models.CharField(max_length=100)
	KH = models.FloatField(null = True, blank = True)
	Fett = models.FloatField(null = True, blank = True)
	Protein = models.FloatField(null = True, blank = True)
	Calories = models.IntegerField(null = True, blank = True)

	def save(self, *args, **kwargs):
		self.Calories = self.Protein*4 + self.KH*4 + self.Fett*9
		super(Food, self).save(*args, **kwargs)
	
	
	def __str__(self):
		return self.lebensmittel





class Meal(models.Model):
	meal_choices = (
		('Breakfast', 'Breakfast'), 
		('Lunch', 'Lunch'),
		('Dinner', 'Dinner'),
		('Snack', 'Snack'),
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	meal = models.CharField(max_length=100,choices= meal_choices, null=True)
	meal_contents = models.ManyToManyField(Food)
	overall_KH = models.FloatField(null = True, blank = True)
	overall_Protein = models.FloatField(null = True, blank = True)
	overall_Fett = models.FloatField(null = True, blank = True)
	overall_Calories = models.FloatField(null = True, blank = True)
	serving_size = models.FloatField(null = True, blank = True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)



	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super().save_model(request, obj, form, change)

	def get_absolute_url(self):
		return reverse('meal-detail', kwargs={'pk': self.pk})


	def __str__(self):
		return self.meal


