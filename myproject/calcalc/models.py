from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Workout(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Workout_choices = (
		('Cardio', 'Cardio'), 
		('Strength', 'Strength'),
		('Circuit', 'Circuit'),
		('Yoga', 'Yoga'),
		)
	workout_duaration_choices = (
		('0 to 30 mins','0 to 30 mins'),
		('30 mins to 1 hour', '30 mins to 1 hour'),
		('1 hour to 1 hour and 30 mins', '1 hour to 1 hour and 30 mins'),
		)
	workout = models.CharField(max_length=10, choices=Workout_choices)
	duaration = models.CharField(max_length=100, choices=workout_duaration_choices)
	# duaration = models.IntegerField(validators=[
 #            MaxValueValidator(120),
 #            MinValueValidator(20)
 #        ])
	calories_burnt = models.IntegerField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	# added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='excersice_username_users')

	def __str__(self):
		return f'{self.user.username} workout'

	# def save_model(self, request, obj, form, change):
	# 	obj.added_by = request.user
	# 	super().save_model(request, obj, form, change)

	def get_absolute_url(self):
		return reverse('workout-detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		if self.workout == "Cardio" and self.duaration == "0 to 30 mins":
			self.calories_burnt = 150
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Cardio" and self.duaration == "30 mins to 1 hour":
			self.calories_burnt = 250
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Cardio" and self.duaration == "1 hour to 1 hour and 30 mins":
			self.calories_burnt = 350
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Strength" and self.duaration == "0 to 30 mins":
			self.calories_burnt = 100
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Strength" and self.duaration == "30 mins to 1 hour":
			self.calories_burnt = 150
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Strength" and self.duaration == "1 hour to 1 hour and 30 mins":
			self.calories_burnt = 200
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Circuit" and self.duaration == "0 to 30 mins":
			self.calories_burnt = 200
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Circuit" and self.duaration == "30 mins to 1 hour":
			self.calories_burnt = 350
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Circuit" and self.duaration == "1 hour to 1 hour and 30 mins":
			self.calories_burnt = 400
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Yoga" and self.duaration == "0 to 30 mins":
			self.calories_burnt = 150
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Yoga" and self.duaration == "30 mins to 1 hour":
			self.calories_burnt = 250
			super(Workout, self).save(*args, **kwargs)

		if self.workout == "Yoga" and self.duaration == "1 hour to 1 hour and 30 mins":
			self.calories_burnt = 350
			super(Workout, self).save(*args, **kwargs)

		

class FitnessGoal(models.Model):
	gender_choices = (
		('Male', 'Male'), 
		('Female', 'Female'),
		)
	activity_level_choices = (('Little', 'Little'),('Moderate', 'Moderate'), ('Extensive', 'Extensive'))
	goal_choices= (('Maintain', 'Maintain'), ('Gain', 'Gain'), ('Lose', 'Lose'))
	age = models.IntegerField()
	gender = models.CharField(max_length=10, choices=gender_choices)
	height = models.IntegerField()
	weight = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	activity_level = models.CharField(max_length=10, choices=activity_level_choices)
	goal = models.CharField(max_length=10, choices=goal_choices)
	goal_calories = models.IntegerField(null=True)
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='username_users')
	optiaml_carbs = models.IntegerField(null=True, blank=True)
	optiaml_fats = models.IntegerField(null=True, blank=True)
	optiaml_proteins = models.IntegerField(null=True, blank=True)



	def __str__(self):
		return str(self.user)

	def save_model(self, request, obj, form, change):
		obj.added_by = request.user
		super().save_model(request, obj, form, change)

	# def save_model(self, request, obj, form, change):
 #    	obj.added_by = request.user
 #    	super().save_model(request, obj, form, change)

	def save(self, *args, **kwargs):
		male_bmr = (10 * self.weight + 6.25 * self.height) - (5 * self.age) + 5
		male_bmr = round(male_bmr)
		female_bmr = (10 * self.weight + 6.25 * self.height) - (5 * self.age) - 161
		female_bmr = round(female_bmr)
		if self.gender == "Male":
			if self.activity_level == "Little":
				if self.goal == "Maintain":
					maintainance = int(male_bmr * 1.2)
					self.goal_calories = maintainance
					self.optiaml_proteins = self.weight 
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(male_bmr * 1.2)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(male_bmr * 1.2)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight 
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
			if self.activity_level == "Moderate":
				if self.goal == "Maintain":
					maintainance = int(male_bmr * 1.5)
					self.goal_calories = maintainance
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(male_bmr * 1.5)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(male_bmr * 1.5)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
			if self.activity_level == "Extensive":
				if self.goal == "Maintain":
					maintainance = int(male_bmr * 1.7)
					self.goal_calories = maintainance
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(male_bmr * 1.7)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(male_bmr * 1.7)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
		if self.gender == "Female":
			if self.activity_level == "Little":
				if self.goal == "Maintain":
					maintainance = int(female_bmr * 1.2)
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(female_bmr * 1.2)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(female_bmr * 1.2)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
			if self.activity_level == "Moderate":
				if self.goal == "Maintain":
					maintainance = int(female_bmr * 1.5)
					self.goal_calories = maintainance
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(female_bmr * 1.5)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(female_bmr * 1.5)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
			if self.activity_level == "Extensive":
				if self.goal == "Maintain":
					maintainance = int(female_bmr * 1.7)
					self.goal_calories = maintainance
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (maintainance * 0.20)/9
					self.optiaml_carbs = (maintainance * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Gain":
					maintainance = int(female_bmr * 1.7)
					gain = int(maintainance + 100)
					self.goal_calories = gain
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (gain * 0.20)/9
					self.optiaml_carbs = (gain * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)
				if self.goal == "Lose":
					maintainance = int(female_bmr * 1.7)
					lose = int(maintainance - 100)
					self.goal_calories = lose
					self.optiaml_proteins = self.weight
					self.optiaml_fats = (lose * 0.20)/9
					self.optiaml_carbs = (lose * 0.40)/4
					super(FitnessGoal, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('calcalc', kwargs={'pk': self.pk})
