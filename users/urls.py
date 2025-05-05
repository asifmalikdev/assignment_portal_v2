from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/admin', views.signup_admin, name = 'signup_admin'),
    path('signup/teacher/', views.signup_teacher, name='signup_teacher'),
    path('signup/student/', views.signup_student, name='signup_student'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_district/<int:district_id>/', views.delete_district, name='delete_district'),
    path('delete_school/<int:school_id>/', views.delete_school, name='delete_school'),


]
