from .views import TeacherDashboardView, CustomTokenObtainPairView,Student_Dashboard_View
from django.urls import path
from . import views

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/admin', views.signup_admin, name = 'signup_admin'),
    path('signup/teacher/', views.signup_teacher, name='signup_teacher'),
    path('signup/student/', views.signup_student, name='signup_student'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student/dashboard/', Student_Dashboard_View.as_view(), name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_district/<int:district_id>/', views.delete_district, name='delete_district'),
    path('delete_school/<int:school_id>/', views.delete_school, name='delete_school'),
    path('delete_class/<int:classroom_id>/', views.delete_class, name='delete_class'),
    path('assignment/delete/<int:pk>/', views.delete_assignment, name='delete_assignment'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),

]
