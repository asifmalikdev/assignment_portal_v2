from django.urls import path
from . import views

urlpatterns = [
    path("districts/", views.DistrictListCreateView.as_view(), name="district-list-create"),
    path("districts/<str:name>/", views.DistrictDetailView.as_view(), name="district-detail"),
]
