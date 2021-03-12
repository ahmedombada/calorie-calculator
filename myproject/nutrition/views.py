from django.shortcuts import render, redirect
from django.db.models import Sum
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Food, Meal
from calcalc.models import FitnessGoal, Workout
from .forms import AddFoodForm #MealForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)
from itertools import chain
from django.utils import timezone
import datetime

class MealCreateView(LoginRequiredMixin, CreateView):
	model = Meal
	fields = ['meal_name','meal_contents', 'serving_size']
	success_message = 'Meal successfully created'


	def form_valid(self, form):
		form.instance.user = self.request.user
		user_selection =  self.request.POST.getlist('meal_contents')
		serving_size = form.cleaned_data['serving_size']
		kh_value = Food.objects.filter(id__in=user_selection).values_list('KH', flat=True)
		Protein_value = Food.objects.filter(id__in=user_selection).values_list('Protein', flat=True)
		Fett_value = Food.objects.filter(id__in=user_selection).values_list('Fett', flat=True)
		form.instance.overall_Protein = round(float(sum(Protein_value)* (serving_size * 0.01)))
		form.instance.overall_Fett = round(float(sum(Fett_value) * (serving_size * 0.01)))
		form.instance.overall_KH = round(float(sum(kh_value) * (serving_size * 0.01)))
		overall_KH = form.instance.overall_KH
		overall_Protein = form.instance.overall_Protein
		overall_Fett = form.instance.overall_Fett
		form.instance.overall_Calories = round(float((overall_KH * 4) + (overall_Protein * 4) + (overall_Fett * 9)))
		return super().form_valid(form)
		

	
	def get_success_url(self):
		if self.request.POST.get('create'):
			return reverse('meal-list')
		elif self.request.POST.get('edit'):
			return reverse('meal-create') 
		else:
			return reverse('meal-list')



class MealUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Meal
	fields = ['meal_name','meal_contents','serving_size']
	# get_success_url = reverse_lazy('/')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		meal = self.get_object()
		if self.request.user == meal.user:
			return True
		return False

class MealListView(LoginRequiredMixin, ListView):
	model = Meal
	queryset = Meal.objects.all()
	context_object_name = 'object'
	# paginate_by = 10


	def get_context_data(self, **kwargs):
		#vars

		today = datetime.date.today()
		start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0) # represents 00:00:00
		end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59) # represents 23:59:59
		start_week = today - datetime.timedelta(today.weekday())
		end_week = start_week + datetime.timedelta(7)


		# Querysets section

		# q1 = Meal.objects.filter(user=self.request.user, ).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		# if q1 is None:
		# 	q1 = 0
		q2 = FitnessGoal.objects.get(user=self.request.user).goal_calories
		if q2 is None:
			q2 = 0
		qs_daily_overall_calories = Meal.objects.filter(user=self.request.user, created_at__range=(start_date, end_date)).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		if qs_daily_overall_calories is None:
			qs_daily_overall_calories = 0

			
		qs_goal_carbs = FitnessGoal.objects.get(user=self.request.user).optiaml_carbs
		qs_goal_proteins = FitnessGoal.objects.get(user=self.request.user).optiaml_proteins
		qs_goal_fats = FitnessGoal.objects.get(user=self.request.user).optiaml_fats
		qs_all_meals= Meal.objects.all()

		qs_daily_carbs_1 = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_daily_carbs_1 is None:
			qs_daily_carbs_1 = 0
		qs_daily_carbs_2 = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_daily_carbs_2 is None:
			qs_daily_carbs_2 = 0
		qs_daily_carbs_3 = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_daily_carbs_3 is None:
			qs_daily_carbs_3 = 0
		qs_daily_carbs_4 = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_daily_carbs_4 is None:
			qs_daily_carbs_4 = 0


		qs_daily_protein_1 = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_daily_protein_1 is None:
			qs_daily_protein_1 = 0
		qs_daily_protein_2 = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_daily_protein_2 is None:
			qs_daily_protein_2 = 0
		qs_daily_protein_3 = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_daily_protein_3 is None:
			qs_daily_protein_3 = 0
		qs_daily_protein_4 = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_daily_protein_4 is None:
			qs_daily_protein_4 = 0

		qs_daily_Fett_1 = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_daily_Fett_1 is None:
			qs_daily_Fett_1 = 0
		qs_daily_Fett_2 = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_daily_Fett_2 is None:
			qs_daily_Fett_2 = 0
		qs_daily_Fett_3 = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_daily_Fett_3 is None:
			qs_daily_Fett_3 = 0
		qs_daily_Fett_4 = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_daily_Fett_4 is None:
			qs_daily_Fett_4 = 0


		qs_br_oac = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		if qs_br_oac is None:
			qs_br_oac = 0
		qs_br_kh = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_br_kh is None:
			qs_br_kh = 0
		qs_br_pr = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_br_pr is None:
			qs_br_pr = 0
		qs_br_f = Meal.objects.filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_br_f is None:
			qs_br_f = 0


		qs_lu_oac = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		if qs_lu_oac is None:
			qs_lu_oac = 0
		qs_lu_kh= Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_lu_kh is None:
			qs_lu_kh = 0
		qs_lu_pr = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_lu_pr is None:
			qs_lu_pr = 0
		qs_lu_f = Meal.objects.filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_lu_f is None:
			qs_lu_f = 0






		qs_di_oac = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		if qs_di_oac is None:
			qs_di_oac = 0
		qs_di_kh = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_di_kh is None:
			qs_di_kh = 0
		qs_di_pr = Meal.objects.filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_di_pr is None:
			qs_di_pr = 0
		qs_di_f = Meal.objects.filter(user=self.request.user, meal_name="Dinner").aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_di_f is None:
			qs_di_f = 0





		qs_s_oac = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Calories'))['overall_Calories__sum']
		if qs_s_oac is None:
			qs_s_oac = 0
		qs_s_kh = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_KH'))['overall_KH__sum']
		if qs_s_kh is None:
			qs_s_kh = 0
		qs_s_pr = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Protein'))['overall_Protein__sum']
		if qs_s_pr is None:
			qs_s_pr = 0
		qs_s_f = Meal.objects.filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date)).aggregate(Sum('overall_Fett'))['overall_Fett__sum']
		if qs_s_f is None:
			qs_s_f = 0


		qs_breakfast = Meal.objects.values('meal_contents').filter(user=self.request.user, meal_name="Breakfast", created_at__range=(start_date, end_date))
		qs_breakfast_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = qs_breakfast)
		qs_lunch = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Lunch", created_at__range=(start_date, end_date)) 
		qs_lunch_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = qs_lunch)
		qs_dinner = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Dinner", created_at__range=(start_date, end_date))
		qs_dinner_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = qs_dinner)
		qs_snack = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Snack", created_at__range=(start_date, end_date))
		qs_snack_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = qs_snack)

		qs_breakfast_meal_ids = list(Meal.objects.filter(user=self.request.user, meal_name="Breakfast").values_list('id', flat=True).order_by('-created_at'))
		qs_lunch_meal_ids = list(Meal.objects.filter(user=self.request.user, meal_name="Lunch").values_list('id', flat=True).order_by('-created_at'))
		qs_dinner_meal_ids = list(Meal.objects.filter(user=self.request.user, meal_name="Dinner").values_list('id', flat=True).order_by('-created_at'))
		qs_snack_meal_ids = list(Meal.objects.filter(user=self.request.user, meal_name="Snack").values_list('id', flat=True).order_by('-created_at'))

		breakfast_meal_contents_ids = zip(qs_breakfast_meal_ids, qs_breakfast_result)
		Lunch_meal_contents_ids = zip(qs_lunch_meal_ids, qs_lunch_result)
		dinner_meal_contents_ids = zip(qs_dinner_meal_ids, qs_dinner_result)
		snack_meal_contents_ids = zip(qs_snack_meal_ids, qs_snack_result)


		workout_count_daily_cardio = Workout.objects.filter(user=self.request.user, created_at__range=(start_date, end_date), workout="Cardio").count()
		if workout_count_daily_cardio is None:
			workout_count_daily_cardio = 0
		workout_count_weekly_cardio = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week),workout="Cardio").count()
		if workout_count_weekly_cardio is None:
			workout_count_weekly_cardio = 0

		workout_count_daily_strength = Workout.objects.filter(user=self.request.user, created_at__range=(start_date, end_date), workout="Strength").count()
		if workout_count_daily_strength is None:
			workout_count_daily_strength = 0
		workout_count_weekly_strength = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week),workout="Strength").count()
		if workout_count_weekly_strength is None:
			workout_count_weekly_strength = 0

		workout_count_daily_circuit = Workout.objects.filter(user=self.request.user, created_at__range=(start_date, end_date), workout="Circuit").count()
		if workout_count_daily_circuit is None:
			workout_count_daily_circuit = 0
		workout_count_weekly_circuit = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week),workout="Circuit").count()
		if workout_count_weekly_circuit is None:
			workout_count_weekly_circuit = 0

		workout_count_daily_yoga = Workout.objects.filter(user=self.request.user, created_at__range=(start_date, end_date), workout="Yoga").count()
		if workout_count_daily_yoga is None:
			workout_count_daily_yoga = 0
		workout_count_weekly_yoga = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week),workout="Yoga").count()
		if workout_count_weekly_yoga is None:
			workout_count_weekly_yoga = 0

		workout_count_weekly_overall = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week)).count()
		if workout_count_weekly_overall is None:
			workout_count_weekly_overall = 0


		#Context section
		context = super(MealListView, self).get_context_data(**kwargs)
		context['breakfast_overall_Calories_queryset'] = qs_br_oac
		context['breakfast_overall_KH'] = qs_br_kh
		context['breakfast_overall_Protein'] = qs_br_pr
		context['breakfast_overall_Fett'] = qs_br_f
		context['lunch_overall_Calories_queryset'] = qs_lu_oac
		context['lunch_overall_KH'] = qs_lu_kh
		context['lunch_overall_Protein'] = qs_lu_pr
		context['lunch_overall_Fett'] = qs_lu_f
		context['dinner_overall_Calories_queryset'] = qs_di_oac
		context['dinner_overall_KH'] = qs_di_kh
		context['dinner_overall_Protein'] = qs_di_pr
		context['dinner_overall_Fett'] = qs_di_f
		context['snack_overall_Calories_queryset'] = qs_s_oac
		context['snack_overall_KH'] = qs_s_kh
		context['snack_overall_Protein'] = qs_s_pr
		context['snack_overall_Fett'] = qs_s_f
		context['daily_overall_Calories'] = qs_daily_overall_calories
		context['goal_calories'] = FitnessGoal.objects.get(user=self.request.user).goal_calories
		context['optimal_carbs'] = qs_goal_carbs
		context['optimal_proteins'] = qs_goal_proteins
		context['optimal_fats'] = qs_goal_fats
		context['remainder'] = q2 - qs_daily_overall_calories		
		context['todays_carbs'] = qs_daily_carbs_1 + qs_daily_carbs_2 + qs_daily_carbs_3 + qs_daily_carbs_4
		context['todays_proteins'] = qs_daily_protein_1 + qs_daily_protein_2 + qs_daily_protein_3 + qs_daily_protein_4
		context['todays_fats'] = qs_daily_Fett_1 + qs_daily_Fett_2 + qs_daily_Fett_3 + qs_daily_Fett_4
		context['breakfast_foods'] = qs_breakfast_result
		context['lunch_foods'] = qs_lunch_result
		context['dinner_foods'] = qs_dinner_result
		context['snack_foods'] = qs_snack_result
		context['meals'] = qs_all_meals
		context['breakfast_ids'] = breakfast_meal_contents_ids
		context['lunch_ids'] = Lunch_meal_contents_ids
		context['dinner_ids'] = dinner_meal_contents_ids
		context['snack_ids'] = snack_meal_contents_ids
		context['cardio_daily'] = workout_count_daily_cardio
		context['cardio_weekly'] = workout_count_weekly_cardio
		context['strength_daily'] = workout_count_daily_strength
		context['strength_weekly'] = workout_count_weekly_strength
		context['circuit_daily'] = workout_count_daily_circuit
		context['circuit_weekly'] = workout_count_weekly_circuit
		context['yoga_daily'] = workout_count_daily_yoga
		context['yoga_weekly'] = workout_count_weekly_yoga
		context['workout_weekly_overall'] = workout_count_weekly_overall
		return context

class MealDetailView(DetailView):
	model = Meal
	# queryset = Meal.objects.all()
	# context_object_name = 'object'

	def get_context_data(self, **kwargs):
		context = super(MealDetailView, self).get_context_data(**kwargs)
		qs_get_meal_name = list(Meal.objects.values_list("meal_name", flat=True).filter(id=self.kwargs['pk'])) #list(Meal.objects.filter(id=self.kwargs['pk']).values_list("meal_name"))
		qs_get_meal_serving = list(Meal.objects.values_list("serving_size", flat=True).filter(id=self.kwargs['pk']))
		qs_get_meal_ids = list(Meal.objects.values_list("meal_contents", flat=True).filter(id=self.kwargs['pk']))
		qs_get_meal_contents = list(Food.objects.values_list("lebensmittel", flat=True).filter(id__in=qs_get_meal_ids))
		meal_detail_list = zip(qs_get_meal_name, qs_get_meal_contents, qs_get_meal_serving)
		context['meals'] = meal_detail_list
		# qs_all_meals= Meal.objects.all()
		# detail_qs_breakfast = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Breakfast")
		# detail_qs_breakfast_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = detail_qs_breakfast)
		# detail_qs_lunch = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Lunch") 
		# detail_qs_lunch_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = detail_qs_lunch)
		# detail_qs_dinner = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Dinner")
		# detail_qs_dinner_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = detail_qs_dinner)
		# detail_qs_snack = Meal.objects.values_list('meal_contents', flat=True).filter(user=self.request.user, meal_name="Snack")
		# detail_qs_snack_result = Food.objects.values_list('lebensmittel', flat=True).filter(id__in = detail_qs_snack)
		# context = super(MealDetailView, self).get_context_data(**kwargs)
		# context['meals'] = qs_all_meals
		# context['breakfast_foods'] = detail_qs_breakfast_result
		# context['lunch_foods'] = detail_qs_lunch_result
		# context['dinner_foods'] = detail_qs_dinner_result
		# context['snack_foods'] = detail_qs_snack_result
		return context


class FoodListView(LoginRequiredMixin, ListView):
	model = Food
	queryset = Food.objects.all()
	context_object_name = 'object'
	paginate_by = 10


def AddFoodView(request):
	if request.method == 'POST':
		form = AddFoodForm(request.POST)
		if form.is_valid():
			KH = form.cleaned_data['KH']
			Protein = form.cleaned_data['Protein']
			Fett = form.cleaned_data['Fett']
			form.save()
			messages.success(request, f'food saved successfully')
	else:
		form = AddFoodForm()
		# calories = None
	return render(request, "nutrition/add_food.html", {'form': form})


# Meal.objects.values_list('meal_contents', flat=True).filter(user="1", meal_name="Breakfast")
# Food.objects.values_list('lebensmittel', flat=True).filter(id__in = result)