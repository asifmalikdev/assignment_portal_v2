from .models import District, School,ClassRoom
from django import forms


class DistrictForm(forms.ModelForm):

    class Meta:
        model = District
        fields = ['name', 'is_active']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address','district', 'principal', 'is_active']

class ClassForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'grade_level', 'school', 'assigned_teacher', 'students', 'is_active']
