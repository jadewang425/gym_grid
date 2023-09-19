from django.db import models
from datetime import date
from django.contrib.auth.models import User

CATEGORIES = (
    (1, 'Abs'), 
    (2, 'Arms'), 
    (3, 'Back'), 
    (4, 'Calves'), 
    (5, 'Cardio'), 
    (6, 'Chest'), 
    (7, 'Legs'), 
    (8, 'Shoulders'),
)

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default=CATEGORIES[0][0]
        )
    equipment = models.CharField(max_length=20)
    weights = models.IntegerField()
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return f"{self.name}: {self.reps} reps x {self.sets} set(s)"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField('workout date')
    duration = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    exercises = models.ManyToManyField(Exercise, related_name='workouts')

    def __str__(self):
        return self.name