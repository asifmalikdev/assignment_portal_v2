from django.urls import path
from . import views

urlpatterns = [
    path("districts/", views.DistrictListCreateView.as_view(), name="district-list-create"),
    path("districts/<str:name>/", views.DistrictDetailView.as_view(), name="district-detail"),
    path("school/", views.SchoolListCreateViwe.as_view(), name="school-list-create"),
    path("school/<str:name>/", views.SchoolDetailView.as_view(), name="school-detail"),
    path("class/", views.ClassRoomListCreateView.as_view(), name="classes")

]
