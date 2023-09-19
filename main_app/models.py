from django.db import models
from datetime import date
from django.urls import reverse
# import user
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField('workout date')
    duration = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    exercises = models.ManyToManyField(Exercise, related_name='workouts')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'workout_id': self.id})

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weights = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.exercise.name} - {self.weights} lbs - {self.reps} reps"