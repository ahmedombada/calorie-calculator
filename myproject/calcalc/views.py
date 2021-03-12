from django.shortcuts import render
from .models import FitnessGoal, Workout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# from .forms import CalorieCalculatorForm
from django.views.generic import (ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)
import datetime
# from django.contrib.auth.decorators import login_required
# Create your views here.


class WorkoutCreateView(LoginRequiredMixin, CreateView):
	model = Workout
	fields = ['workout', 'duaration']
	success_message = 'Workout added successfully'
	success_url = reverse_lazy('workout-list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class WorkoutDetailView(LoginRequiredMixin, DetailView):
	model = Workout
	

class WorkoutUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Workout
	fields = ['workout', 'duaration']
	success_message = 'Workout added successfully'
	success_url = reverse_lazy('workout-detail')
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		goal = self.get_object()
		if self.request.user == goal.user:
			return True
		return False
		
class WorkoutListView(LoginRequiredMixin, ListView):
	model = Workout
	queryset = Workout.objects.all()

	def get_context_data(self, **kwargs):
		#vars
		today = datetime.date.today()
		start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0) # represents 00:00:00
		end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59) # represents 23:59:59

		start_week = today - datetime.timedelta(today.weekday())
		end_week = start_week + datetime.timedelta(7)


		#queries
		qs_daily_workouts = Workout.objects.filter(user=self.request.user, created_at__range=(start_date, end_date))
		qs_weekly_workouts = Workout.objects.filter(user=self.request.user, created_at__range=(start_week, end_week))
		#contexts
		context = super(WorkoutListView, self).get_context_data(**kwargs)
		context['daily_workouts'] = qs_daily_workouts
		context['weekly_workouts'] = qs_weekly_workouts
		return context

	# def get_queryset(self):
	# 	today = datetime.date.today()
	# 	start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0) # represents 00:00:00
	# 	end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59) # represents 23:59:59
	# 	return self.model.objects.filter(user=self.request.user,created_at__range=(start_date, end_date))




class GoalListView(LoginRequiredMixin, ListView):
	model = FitnessGoal
	queryset = FitnessGoal.objects.all()
	context_object_name = 'object'

	def get_queryset(self):
		return self.model.objects.filter(user=self.request.user)

	# def get_context_data(self, **kwargs):

	# 	return context

# class GoalDetailView(LoginRequiredMixin, DetailView):
# 	model = FitnessGoal
# 	queryset = FitnessGoal.objects.all()
# 	context_object_name = 'object'
	

class GoalCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
	model = FitnessGoal
	fields = ['age', 'height', 'weight', 'gender', 'activity_level', 'goal']
	success_message = 'goal successfully created'
	success_url = reverse_lazy('goal-breakdown')



	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class GoalUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = FitnessGoal
	fields = ['weight', 'height', 'activity_level', 'goal']
	success_message = 'goal successfully updated'
	success_url = reverse_lazy('goal-breakdown')


	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		goal = self.get_object()
		if self.request.user == goal.user:
			return True
		return False
