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
from .models import Workout, Exercise, Photo
from .forms import AddExerciseForm

# for adding photos we need more imports
import uuid
import boto3
import os

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

# adding photos via s3
def add_photo(request, exercise_id):
    # we need a photo file (named via the 'name' attribute in the form field)
    photo_file = request.FILES.get('photo-file', None)
    AWS_ACCESS_Key = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_ACCESS_Key = os.environ['AWS_SECRET_ACCESS_KEY']
    #check if we actually got a photo, do something if we did, do something else if we didn't
    if photo_file:
        #here's where we'll do our S3 stuff
        #target s3
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_Key,
         aws_secret_access_key=AWS_SECRET_ACCESS_Key)
        # we need a unique name for all of our files, so we'll use uuid to 
        # generate one automatically
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # we'll build the entire url string
            url = f'{os.environ["S3_BASE_URL"]}{bucket}/{key}'
            # we create the photo and associate it with the exercise
            Photo.objects.create(url=url, exercise_id=exercise_id)
        except Exception as e:
            print('An error occurred uploading to s3')
        return redirect('detail', exercise_id=exercise_id)