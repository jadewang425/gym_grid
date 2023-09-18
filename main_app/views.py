from django.shortcuts import render, redirect

# Import CBV's
from django.views.generic.edit import HomeView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView

# Import Models
from .models import Workout, Exercise, Set

# Create your views here.
class Home(HomeView):
    template_name = 'home.html'

class WorkoutList(ListView):
    model = Workout
    template_name = 'workouts/index.html'

class WorkoutDetail(DetailView):
    model = Workout
    template_name = 'workouts/detail.html'

class WorkoutCreate(CreateView):
    model = Workout
    fields = '__all__'
    success_url = '/workouts/{workout_id}'

class WorkoutUpdate(UpdateView):
    model = Workout 
    fields = '__all__'

class WorkoutDelete(DeleteView):
    model = Workout
    success_url = '/workouts'
