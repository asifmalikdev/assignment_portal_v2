from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from school.models import ClassRoom
from .models import Assignment, AssignmentQuestion, AssignmentQuestionThrough


class AssignmentQuestionInLineForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestion
        fields = ('assigned_class', 'text', 'question_type', 'marks', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option')

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.teacher and self.user:
            self.instance.teacher = self.user
        question_type = cleaned_data.get('question_type')
        if question_type == 'MCQ':
            required = ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
            for field in required:
                if not cleaned_data.get(field):
                    raise ValidationError('All options and the correct answer are required for MCQs.')
        elif question_type in ['SHORT', 'LONG']:
            for option_field in ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']:
                if cleaned_data.get(option_field):
                    self.add_error(option_field, 'Options are only allowed for MCQ type questions.')

        return cleaned_data




        return cleaned_data
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['assigned_class'].queryset = ClassRoom.objects.filter(assigned_teacher=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.teacher = self.user
        if commit:
            instance.save()
        return instance

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'assigned_class', 'due_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.role == "teacher":
            self.fields['assigned_class'].queryset = self.request.user.teaching_classes.all()

    def clean(self):
        cleaned_data = super().clean()
        assigned_class = cleaned_data.get("assigned_class")
        if self.request and not self.request.user.teaching_classes.filter(pk=assigned_class.pk).exists():
            raise ValidationError("You are not allowed to assign for this class.")
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.teacher_id and self.request:
            obj.teacher = self.request.user
        if commit:
            obj.save()
        return obj


class AssignmentQuestionThroughForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestionThrough
        fields = '__all__'


AssignmentQuestionThroughInlineFormset = inlineformset_factory(
    Assignment,
    AssignmentQuestionThrough,
    form=AssignmentQuestionThroughForm,
    extra=1,
    can_delete=True
)
from .models import AssignmentSubmission, StudentAnswer, AssignmentQuestion

class AssignmentSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment')
        super().__init__(*args, **kwargs)
        for question in self.assignment.questions.all():
            field_name = f"question_{question.id}"
            if question.question_type == 'MCQ':
                choices = [
                    ('a', question.option_a),
                    ('b', question.option_b),
                    ('c', question.option_c),
                    ('d', question.option_d),
                ]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=True
                )
            else:
                self.fields[field_name] = forms.CharField(
                    label=question.text,
                    widget=forms.Textarea,
                    required=True
                )

