from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_assignment, name='create_assignment'),
    path('submit/', views.submit_assignment, name='submit_assignment'),
]
