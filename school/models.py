import re
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import CASCADE

User = get_user_model()

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="District Name")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip()
        self.name = self.name.lower()
        if len(self.name) < 4:
            raise ValidationError("District name must contain atleast 4 character")
        if not re.match(r'^[a-z\s]+$', self.name):
            raise ValidationError("Name must contain letters only")

class School(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255, unique=True, verbose_name="School")
    address = models.TextField(verbose_name="Address")
    principal = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=CASCADE, related_name="school_district")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    def __str__(self):
        return self.name
    def clean(self):
        self.name = self.name.strip().lower()
        if not re.match(r'^[a-zA-Z\s]+$', self.name):
            raise ValidationError("Only letter Please")
        if len(self.address.strip())<10:
            raise ValidationError("Address Must Contain Atleast 10 Character")

def validate_grade_level(value):
    if value < 1 or value > 12:
        raise ValidationError("Grade level must be between 1 and 12.")

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    grade_level= models.IntegerField(validators=[validate_grade_level])
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    assigned_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_classes'
    )
    students = models.ManyToManyField(
        User,
        blank=True,
        limit_choices_to={'role': 'student'},
        related_name='enrolled_classes'
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('name', 'school')  #here ensuring classname should be unique, we fullfilled one section or multiple section requirements here

    def clean(self):
        self.name = self.name.strip()

        if self.school and not self.school.is_active:
            raise ValidationError("Cannot assign class to an inactive school.")

        if len(self.name) < 2:
            raise ValidationError("Class name must be at least 2 characters long.")

    def __str__(self):
        return f"{self.name} - Grade {self.grade_level} ({self.school.name})"