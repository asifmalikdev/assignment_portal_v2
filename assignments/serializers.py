from rest_framework.exceptions import ValidationError

from .models import AssignmentQuestion
from rest_framework import serializers

class AssignmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentQuestion
        fields = '__all__'
        read_only_fields = ['teacher', 'create_at']

    def validate(self, data):
        request = self.context['request']
        user = request.user

        assigned_class = data.get('assigned_class')
        if user.role == 'teacher':
            if assigned_class.assigned_teacher != user:
                raise ValidationError("Teacher can't assigned question to this class")

        questions_types = data.get('question_type')
        options = [data.get("option_a"), data.get("option_b"), data.get("option_c"), data.get("option_d")]
        correct_option = data.get("correct_option")
        if questions_types == "MCQ":
            if not all(options) or not correct_option:
                raise ValidationError("MCQ required option and correct answer")

        elif questions_types != "MCQ":
            if any(options) or correct_option:
                raise ValidationError("Options are not valid in Subjective type questions")
        return data

