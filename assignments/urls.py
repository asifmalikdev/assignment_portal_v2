from django.urls import path
from .views import (
    AssignmentCreateView,
    StudentAssignmentListView,
    AssignmentSubmitView
)

urlpatterns = [
    path("create/", AssignmentCreateView.as_view(), name="assignment_create"),
    path("student/", StudentAssignmentListView.as_view(), name="student_assignments"),
    path("submit/<int:assignment_id>/", AssignmentSubmitView.as_view(), name="submit_assignment"),
]
