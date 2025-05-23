from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import District, School, ClassRoom
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'is_active']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields= '__all__'

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

    def validate(self,data):
        school=data.get("school")
        teacher = data.get("assigned_teacher")
        students=data.get("students")
        if teacher and teacher.school != school:
            raise ValidationError("This Teacher does not belong to this school")
        for student in students:
            if student.school != school:
                raise ValidationError({
                    "students": f"Student '{student.full_name}' does not belong to the selected school."
                })
        return data