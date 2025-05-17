from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CASCADE
from school.models import ClassRoom
from django.utils import timezone

User = get_user_model()


class AssignmentQuestion(models.Model):
    QUESTION_TYPE_CHOICES=[
        ('LONG', 'Long Question'),
        ('SHORT', 'Short Question'),
        ('MCQ', 'Multiple Choice')
    ]

    teacher = models.ForeignKey(
        User,
        on_delete= CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name= 'questions'
    )
    assigned_class = models.ForeignKey(ClassRoom, on_delete=CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=5, choices = QUESTION_TYPE_CHOICES)
    marks = models.PositiveIntegerField()

    option_a = models.CharField(max_length = 255, blank = True, null = True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)

    correct_option = models.CharField(
        max_length=1,
        choices = [('a','A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
        null=True,
        blank=True,


    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.question_type == 'MCQ':
            if not all([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError("All options and Correct answers must be provided")
        if self.question_type in ['LONG', 'SHORT']:
            if any([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError("Options are only allowed for MCQ")
        if self.teacher and self.assigned_class_id:
            if self.assigned_class.assigned_teacher_id != self.teacher_id:
                raise ValidationError("You are not assigned to this class")

    def __str__(self):
        return f"{self.text[:30]} - {self.get_question_type_display()} ({self.assigned_class.name})"

def validate_due_date(value):
    if value < timezone.now():
        raise ValidationError("Due date can't be in the past.")



class Assignment(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    due_date = models.DateTimeField(validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        User,
        on_delete=CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='assignments',
        blank=True,
        null=True

    )
    assigned_class = models.ForeignKey(
        ClassRoom,
        on_delete=CASCADE,
        related_name='assignments')
    questions = models.ManyToManyField(
        AssignmentQuestion,
        through = 'AssignmentQuestionThrough',
        related_name = 'assignments'
    )
    # def clean(self):
    #     if not self.teacher.teaching_classes.filter(pk = self.assigned_class.pk).exists():
    #         raise ValidationError("this teacher is not assigned to the selected class")

    def __str__(self):
        return f"{self.title}({self.assigned_class.name})"

class AssignmentQuestionThrough(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE)
    question = models.ForeignKey(AssignmentQuestion, on_delete=CASCADE)
    # Optional: order or custom mark settings
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('assignment', 'question')

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=CASCADE,
        limit_choices_to={'role':'student'},
        related_name='submissions'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=CASCADE,
        related_name="submission"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_grade = models.BooleanField(default=False)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', "assignment")
    def __str__(self):
        return f"{self.student.full_name} - {self.assignment.title}"


class StudentAnswer(models.Model):
    submission = models.ForeignKey(
        AssignmentSubmission,
        on_delete=CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        AssignmentQuestion,
        on_delete=CASCADE
    )
    answer_text = models.TextField(blank=True, null=True)
    select_option = models.CharField(
        max_length=1,
        choices=[('a','A'),('b','B'),('c','C'),('d','D')],
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.submission.student.full_name} - Q: {self.question.text}"














