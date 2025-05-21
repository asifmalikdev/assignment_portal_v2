from rest_framework.exceptions import ValidationError
from urllib3 import request

from .models import AssignmentQuestion, Assignment
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

class AssignmentSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AssignmentQuestion.objects.all()
    )
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'assigned_class', 'questions']
    def validate(self,data):
        request = self.context['request']
        user = request.user
        class_ = data.get("assigned_class")
        questions = data.get("questions")
        for question in questions:
            if question.teacher != request.user:
                raise ValidationError(f"Question '{question}' is not from this teacer book")
            if question.assigned_class != class_:
                raise ValidationError(f"Question '{question}' is not for the current '{class_}' but for {question.assigned_class}")
            print("Question Class: ",question.assigned_class, "\nClass : ", class_)
        if class_.assigned_teacher != request.user:
            raise ValidationError("This teacher is not teaching to this class")
        # print("data : ",data, "\nUser : ", user, "class assign is being assigned to : ", class_)

        return data