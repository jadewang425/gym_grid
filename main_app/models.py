from django.db import models
from datetime import date
from django.urls import reverse

# import user
from django.contrib.auth.models import User

import requests

# CATEGORIES = (
#     ('abs', 'Abs'), 
#     ('arms', 'Arms'), 
#     ('back', 'Back'), 
#     ('calves', 'Calves'), 
#     ('cardio', 'Cardio'), 
#     ('chest', 'Chest'), 
#     ('legs', 'Legs'), 
#     ('shoulders', 'Shoulders')
# )

# function to return API data as a tuple of two-tuples for equipment dropdown
def get_eqpt_lst():
    response = requests.get('https://wger.de/api/v2/equipment')
    objects = response.json()
    lst_obj = objects['results']
    equipments = [(i['id'], i['name']) for i in lst_obj]
    return tuple(equipments)

def get_eqpt_lst():
    response = requests.get('https://wger.de/api/v2/exercisecategory/')
    objects = response.json()
    lst_obj = objects['results']
    category = [(i['id'], i['name']) for i in lst_obj]
    return tuple(category)

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=20,
        choices=get_eqpt_lst(),
        default=get_eqpt_lst()[0][0],
    )
    equipment = models.CharField(
        max_length=20,
        choices=get_eqpt_lst(),
        default=get_eqpt_lst()[0][0],
    )
    weights = models.IntegerField()
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):

        return f"{self.name}: {self.reps} reps x {self.sets} set(s)"
    
    def get_absolute_url(self):
        return reverse('exercises_detail', kwargs={'pk': self.id})

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