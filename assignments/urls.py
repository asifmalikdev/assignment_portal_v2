from django.urls import path
from . import views

urlpatterns = [
    path('assignment_create_view/', views.assignment_create_view, name='assignment_create_view'),
    path('submit/', views.submit_assignment, name='submit_assignment'),
]
