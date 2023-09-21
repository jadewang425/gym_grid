from django.shortcuts import render, redirect

# Import CBV's
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

# Import Models
from .models import Workout, Exercise
from .forms import AddExerciseForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def workouts_index(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workouts/index.html', { 'workouts': workouts})

@login_required
def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises_id = workout.exercises.all().values_list('id')
    exercises = Exercise.objects.exclude(id__in=exercises_id)
    add_exercise_form = AddExerciseForm()
    return render(request, 'workouts/detail.html', {'workout': workout, 'add_exercise_form': add_exercise_form, 'exercises': exercises})


class WorkoutCreate(LoginRequiredMixin, CreateView):
    model = Workout
    fields = ['name', 'date', 'duration', 'description', 'exercises']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdate(LoginRequiredMixin, UpdateView):
    model = Workout 
    fields = '__all__'

class WorkoutDelete(LoginRequiredMixin, DeleteView):
    model = Workout
    success_url = '/workouts'

class ExerciseList(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = 'exercises/index.html'

class ExerciseDetail(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = 'exercises/detail.html'

class ExerciseCreate(LoginRequiredMixin, CreateView):
    model = Exercise
    fields = '__all__'

class ExerciseUpdate(LoginRequiredMixin, UpdateView):
    model = Exercise
    fields = '__all__'

class ExerciseDelete(LoginRequiredMixin, DeleteView):
    model = Exercise
    success_url = '/exercises/'

def add_exercise(request, workout_id, exercise_id):
    form = AddExerciseForm(request.POST)
    print('add_exercise_func', form)
    workout = Workout.objects.get(id=workout_id)
    if form.is_valid():
        workout.exercises.add(exercise_id)
        return render('detail', workout_id=workout_id)

# associate exercise to a workout
def assoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.add(exercise_id)
    return redirect('detail', workout_id=workout_id)

def unassoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.remove(exercise_id)
    return redirect('detail', workout_id=workout_id)

# signup
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the date from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
        
    # A bad POST or GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)