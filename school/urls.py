from django.urls import path
from . import views

urlpatterns=[
    path("District_List/", views.District_List.as_view(), name="Add_District_api"),
    path("District_List/<int:pk>",views.District_List.as_view(), name="Add_District_api")
]