from django.urls import path
from . import views
from .views import StudentAssignment, AssignmentSubmitView, StudentAssignmentListView

urlpatterns = [
    path('assignment_create_view/', views.AssignmentCreateView.as_view(), name='assignment_create_view'),
    path('submit/', views.submit_assignment, name='submit_assignment'),
    path('assignments_page/', StudentAssignment.as_view(), name="assignments_page"),
    path('student/list/', StudentAssignmentListView.as_view(), name='assignments_page'),

    path('submit/<int:assignment_id>/', AssignmentSubmitView.as_view(), name='submit_assignment'),

]
