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
        print("asif malik in serializer class")
        model = ClassRoom
        fields = '__all__'

    def validate(self,data):
        print("asif malik in serializer functions")
        school=data.get("school")
        teacher = data.get("assigned_teacher")
        students=data.get("students")
        print("asif")
        if teacher and teacher.school != school:
            print("malik")
            raise ValidationError("This Teacher does not belong to this school")
        for student in students:
            if student.school != school:
                print("channar")
                raise ValidationError({
                    "students": f"Student '{student.full_name}' does not belong to the selected school."
                })
        return data