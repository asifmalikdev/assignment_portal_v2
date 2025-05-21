from django.urls import path
from .views import (
    AssignmentCreateView,
    StudentAssignmentListView,
    AssignmentSubmitView, AssignmentQuestionListCreateAPIView, AssignmentQuestionDetailAPIView, AssignmentListCreate,
    AssignmentDetailView
)

urlpatterns = [
    path("create/", AssignmentCreateView.as_view(), name="assignment_create_view"),
    path("student/", StudentAssignmentListView.as_view(), name="student_assignments"),
    path("submit/<int:assignment_id>/", AssignmentSubmitView.as_view(), name="submit_assignment"),
    path('assignment-questions/', AssignmentQuestionListCreateAPIView.as_view(), name='assignment-question-list-create'),
    path('assignment-questions/<int:pk>/', AssignmentQuestionDetailAPIView.as_view(), name='assignment-question-list-create'),
    path('assignments/', AssignmentListCreate.as_view(), name = "assignment-list-create"),
    path("assignments/<int:pk>/", AssignmentDetailView.as_view(), name = "assignment-detail"),
]
