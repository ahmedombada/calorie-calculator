from django.urls import path
from .views import MealListView
from . import views 

urlpatterns = [
	path ('nutriton/', MealListView.as_view(), name='nutriotion'),
]