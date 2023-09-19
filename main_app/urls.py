from django.urls import path
from . import views


urlpatterns = [
    # Workout Home, Index, Detail 
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('workouts/', views.workouts_index, name='index'),
    path('workouts/<int:workout_id>', views.workouts_detail, name='detail'),
    # Workout Create, Update, Delete
    path('workouts/create/', views.WorkoutCreate.as_view(), name='workouts_create'),
    path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workouts_update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workouts_delete'),
    # Exercise List, Create, Update, Delete
    path('exercises/', views.ExerciseList.as_view(), name='exercises_index'),
    path('exercises/<int:pk>/', views.ExerciseDetail.as_view(), name='exercises_detail'),
    path('exercises/create/', views.ExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercises_update'),
    path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercises_delete'),
]