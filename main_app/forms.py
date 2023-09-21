from django.forms import ModelForm
from .models import Workout

class AddExerciseForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['exercises']