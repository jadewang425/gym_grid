from django.shortcuts import render, redirect

# Import CBV's
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Import Models
from .models import Workout, Exercise
from .forms import ExerciseForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def workouts_index(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts/index.html', { 'workouts': workouts})

def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises_id = workout.exercises.all().values_list('id')
    exercises = Exercise.objects.exclude(id__in=exercises_id)
    exercise_form = ExerciseForm()
    return render(request, 'workouts/detail.html', {'workout': workout, 'exercise_form': exercise_form, 'exercises': exercises})

class WorkoutCreate(CreateView):
    model = Workout
    fields = ['name', 'date', 'duration', 'description']

class WorkoutUpdate(UpdateView):
    model = Workout 
    fields = '__all__'

class WorkoutDelete(DeleteView):
    model = Workout
    success_url = '/workouts'

class ExerciseList(ListView):
    model = Exercise
    template_name = 'exercises/index.html'

class ExerciseDetail(DetailView):
    model = Exercise
    template_name = 'exercises/detail.html'

class ExerciseCreate(CreateView):
    model = Exercise
    fields = '__all__'

class ExerciseUpdate(UpdateView):
    model = Exercise
    fields = '__all__'

class ExerciseDelete(DeleteView):
    model = Exercise
    success_url = '/exercises/'

def add_exercise(request, workout_id):
    form = ExerciseForm(request.POST)
    if form.is_valid():
        new_exercise = form.save(commit=False)
        new_exercise.workout_id = workout_id
        new_exercise.save()
        return render('detail', workout_id=workout_id)

# associate exercise to a workout
def assoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.add(exercise_id)
    return redirect('detail', workout_id=workout_id)

def unassoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.remove(exercise_id)
    return redirect('detail', workout_id=workout_id)