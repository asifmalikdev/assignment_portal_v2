from django import forms
from django.core.exceptions import ValidationError
from .models import AssignmentQuestion


class AssignmentQuestionInLineForm(forms.Model):
    class Meta:
        model = AssignmentQuestion
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('question_type')  == 'MCQ':
            required = ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
            for field in required:
                if not cleaned_data.get(field):
                    raise ValidationError('All Options are correct answers are required')
        if cleaned_data.get('question_type') == 'SHORT' or cleaned_data.get('question_type') == 'LONG':
            for option_field in ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']:
                if cleaned_data.get(option_field):
                    self.add_error(option_field, 'Options are only allowed for MCQ type questions.')


        return cleaned_data