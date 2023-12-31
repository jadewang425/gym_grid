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
    equipments = [(i['name'], i['name']) for i in lst_obj]
    return tuple(equipments)

def get_ctgy_lst():
    response = requests.get('https://wger.de/api/v2/exercisecategory/')
    objects = response.json()
    lst_obj = objects['results']
    category = [(i['name'], i['name']) for i in lst_obj]
    return tuple(category)

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=50,
        choices=get_ctgy_lst(),
        default=get_ctgy_lst()[0][0],
    )
    equipment = models.CharField(
        max_length=50,
        choices=get_eqpt_lst(),
        default=get_eqpt_lst()[0][0],
    )
    weights = models.IntegerField()
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return f"{self.name}: {self.reps} reps x {self.sets} set(s) using {self.weights}lb weights. Equipment used: {self.equipment}. Muscle group targeted is {self.category}."
    def get_absolute_url(self):
        return reverse('exercises_detail', kwargs={'pk': self.id})
    
    class Meta:
        ordering = ['name']

class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField('workout date')
    duration = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    exercises = models.ManyToManyField(Exercise)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'workout_id': self.id})
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for exercise_id: {self.exercise} @{self.url}'