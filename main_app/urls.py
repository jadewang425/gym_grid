from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # Workout Index Route
    path('workouts/', views.workouts_index, name='index'),
    # Workout Detail Route
    path('workouts/<int:workout_id>', views.workouts_detail, name='detail'),
]