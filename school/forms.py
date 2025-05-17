from django.core.exceptions import ValidationError

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
    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        teacher = cleaned_data.get('assigned_teacher')
        students = cleaned_data.get('students')
        if teacher and teacher.school != school:
            raise ValidationError("Assigned Teacher Does Not Belong to this school")
        for student in students:
            if student.school != school:
                raise ValidationError(f"Student '{student.full_name}' does not belong to this school")