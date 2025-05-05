from django.shortcuts import render, redirect, get_object_or_404
from .forms import  DistrictForm
from .models import District
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


