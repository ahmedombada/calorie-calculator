"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static
from calcalc import views as calcalc_views
from nutrition import views as nutrition_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    # path('calculator/', calcalc_views.calculator, name='calculator'),
    path('nutrition/', nutrition_views.FoodListView.as_view(), name='nutrition'),
    path('nutrition/addfood/', nutrition_views.AddFoodView, name='addfood'),
    # path('nutrition/addmeal/', nutrition_views.AddMealView, name='addmeal'),
    path('goal/breakdown', calcalc_views.GoalListView.as_view(), name='goal-breakdown'),
    path('create_goal/',calcalc_views.GoalCreateView.as_view(), name='goal-creat'),
    path('', nutrition_views.MealListView.as_view(), name='meal-list'),
    path('nutrition/addmeal',nutrition_views.MealCreateView.as_view(), name='meal-create'),
    path('nutrition/<int:pk>/detail/',nutrition_views.MealDetailView.as_view(), name='meal-detail'),
    path('nutrition/<int:pk>/update/',nutrition_views.MealUpdateView.as_view(), name='meal-update'),
    path('calcalc/<int:pk>/update/',calcalc_views.GoalUpdateView.as_view(), name='calcalc-update'),
    path('workout/add/',calcalc_views.WorkoutCreateView.as_view(), name='workout-add'),
    path('workout/<int:pk>/update/',calcalc_views.WorkoutUpdateView.as_view(), name='workout-update'),
    path('workout/<int:pk>/detail/',calcalc_views.WorkoutDetailView.as_view(), name='workout-detail'),
    path('workout/list', calcalc_views.WorkoutListView.as_view(), name='workout-list'),
    path('', include('blog.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)