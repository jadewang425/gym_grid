from django.urls import path
from . import views


urlpatterns = [
    # Workout Home, Index, Detail 
    path('', views.home, name='home'),
    path('workouts/', views.workouts_index, name='index'),
    path('workouts/<int:workout_id>', views.workouts_detail, name='detail'),
    # Workout Create, Update, Delete
    path('workouts/create/', views.WorkoutCreate.as_view(), name='workouts_create'),
    path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workouts_update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workouts_delete'),
]