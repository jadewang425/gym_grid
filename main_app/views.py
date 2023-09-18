from django.shortcuts import render, redirect


# Import Models
from.models import Workout, Exercise, Set

# Create your views here.
def home(request):
    return render(request, 'home.html')

def workouts_index(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts/index.html', { 'workouts': workouts})

def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    # add form here
    return render(request, 'workouts/detail.html', {'workout': workout})
