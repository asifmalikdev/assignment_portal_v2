from django.contrib import admin
from rest_framework.exceptions import PermissionDenied
from .models import AssignmentQuestion, AssignmentQuestionThrough, Assignment
from .forms import AssignmentForm, AssignmentQuestionThroughInlineFormset


class AssignmentQuestionInline(admin.TabularInline):
    model = AssignmentQuestionThrough
    formset = AssignmentQuestionThroughInlineFormset
    extra = 1


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentForm
    inlines = [AssignmentQuestionInline]
    list_display = ('title', 'teacher', 'assigned_class', 'due_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('teacher', 'assigned_class')

    def save_model(self, request, obj, form, change):
        if not obj.teacher_id and not request.user.is_superuser:
            obj.teacher = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)


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
        if not obj.teacher_id and not request.user.is_superuser:
            obj.teacher = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)
