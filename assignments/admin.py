from django.contrib import admin
from rest_framework.exceptions import PermissionDenied

from .models import AssignmentQuestion
from django import forms

@admin.register(AssignmentQuestion)
class AssignmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'teacher', 'marks', 'question_type', 'created_at', 'assigned_class')
    ordering = ('created_at',)
    list_filter = ('teacher', 'question_type', 'assigned_class')
    search_fields = ('text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.role == 'teacher':
            qs = qs.filter(teacher=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if request.user.role != 'teacher':
                raise PermissionDenied("Only teachers can create assignment questions.")
            if not obj.teacher_id:
                obj.teacher = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)


