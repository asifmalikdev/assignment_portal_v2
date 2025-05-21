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
    list_display = ('id','title', 'teacher', 'assigned_class', 'due_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('teacher', 'assigned_class')

    def save_model(self, request, obj, form, change):
        if not obj.teacher_id and not request.user.is_superuser:
            obj.teacher = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(AssignmentQuestion)
class AssignmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'teacher', 'marks', 'question_type', 'created_at', 'assigned_class')
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
from django.contrib import admin
from .models import AssignmentSubmission, StudentAnswer, Assignment, AssignmentQuestion

class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ('question', 'answer_text', 'select_option')
    can_delete = False

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'is_grade', 'total_score')
    list_filter = ('assignment', 'is_grade')
    search_fields = ('student__full_name', 'assignment__title')
    inlines = [StudentAnswerInline]

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'answer_text', 'select_option')
    list_filter = ('question__question_type',)
    search_fields = ('submission__student__full_name', 'question__text')
