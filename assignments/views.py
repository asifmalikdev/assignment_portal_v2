from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import  FormView
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Assignment, AssignmentQuestionThrough, AssignmentSubmission, StudentAnswer, AssignmentQuestion
from .forms import AssignmentForm, AssignmentSubmissionForm
from .serializers import AssignmentQuestionSerializer, AssignmentSerializer
from rest_framework import status

from assignment_portal.constant import UserRole

class AssignmentCreateView(LoginRequiredMixin, FormView):
    login_url = "/"
    template_name = "assignment_create_template.html"
    form_class = AssignmentForm
    success_url = reverse_lazy("teacher_dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_book"] = AssignmentQuestion.objects.filter(teacher=self.request.user)
        return context

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.teacher = self.request.user
        assignment.save()
        selected_question_ids = self.request.POST.getlist("questions")
        for order, qid in enumerate(selected_question_ids):
            AssignmentQuestionThrough.objects.create(
                assignment=assignment,
                question_id=qid,
                order=order
            )
        return super().form_valid(form)


from django.views.generic import ListView

class StudentAssignmentListView(ListView):
    model = Assignment
    template_name = 'student_assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        user = self.request.user
        return Assignment.objects.filter(
            assigned_class__students=user,
            due_date__gte=timezone.now()
        ).order_by('due_date')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return HttpResponseForbidden("You are not allowed to view this page.")
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, AssignmentSubmission, StudentAnswer
from .forms import AssignmentSubmissionForm
from django.views import View

class AssignmentSubmitView(View):
    template_name = "submit_assignment.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_assignment(self, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        if not assignment.assigned_class.students.filter(id=self.request.user.id).exists():
            return None
        return assignment

    def get(self, request, assignment_id):
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return HttpResponseForbidden("You are not enrolled in this class.")
        if AssignmentSubmission.objects.filter(student=request.user, assignment=assignment).exists():
            return HttpResponse("You have already submitted this assignment.")
        form = AssignmentSubmissionForm(assignment=assignment)
        return render(request, self.template_name, {'form': form, 'assignment': assignment})

    def post(self, request, assignment_id):
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return HttpResponseForbidden("You are not enrolled in this class.")
        if assignment.due_date < timezone.now():
            return HttpResponse("Submission deadline has passed.")
        if AssignmentSubmission.objects.filter(student=request.user, assignment=assignment).exists():
            return HttpResponse("You have already submitted this assignment.")
        form = AssignmentSubmissionForm(request.POST, assignment=assignment)
        if form.is_valid():
            submission = AssignmentSubmission.objects.create(
                student=request.user,
                assignment=assignment
            )
            for question in assignment.questions.all():
                answer_value = form.cleaned_data.get(f"question_{question.id}")
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    answer_text=answer_value if question.question_type != 'MCQ' else None,
                    select_option=answer_value if question.question_type == 'MCQ' else None
                )
            messages.success(request, "Your assignment was submitted successfully.")
            return redirect('student_dashboard')
        return render(request, self.template_name, {'form': form, 'assignment': assignment})

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacherOrAdmin, IsTeacherUser


class AssignmentQuestionListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        user = request.user
        if user.role == UserRole.TEACHER.value:
            question_book = AssignmentQuestion.objects.filter(teacher=user)
        elif user.role == UserRole.ADMIN.value:
            question_book = AssignmentQuestion.objects.all()
        else:
            return Response({"msg": "Permission denied, insufficient role"}, status=status.HTTP_403_FORBIDDEN)

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(question_book, request)
        serializer = AssignmentQuestionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if request.user.role != UserRole.TEACHER.value:
            return Response({"msg": "Only teachers can post questions"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentQuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AssignmentQuestionDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherUser]

    def get(self, request, pk):
        question = get_object_or_404(AssignmentQuestion, pk=pk)
        serializer = AssignmentQuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        question = get_object_or_404(AssignmentQuestion, pk=pk)
        if question.teacher != request.user:
            return Response({"msg": "You are not authorized to update this question."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentQuestionSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data has been successfully updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = get_object_or_404(AssignmentQuestion, pk=pk)
        if question.teacher != request.user:
            return Response({"msg": "You are not authorized to delete this question."}, status=status.HTTP_403_FORBIDDEN)

        question.delete()
        return Response({"msg": "Question deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class AssignmentListCreate(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        user = request.user
        if user.role == UserRole.TEACHER.value:
            assignments = Assignment.objects.filter(teacher=user)
        elif user.role == UserRole.ADMIN.value:
            assignments = Assignment.objects.all()
        else:
            return Response({"msg": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(assignments, request)
        serializer = AssignmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        if request.user.role != UserRole.TEACHER.value:
            return Response({"msg": "Only teachers can create assignments"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():

            assignment = serializer.save(teacher=request.user)

            return Response({"msg": "Assignment has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentDetailView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if assignment.teacher != request.user:
            return Response({"msg": "Access denied for this teacher"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if request.user.role != UserRole.TEACHER.value:
            return Response({"msg": "You are not authorized to update assignments"}, status=status.HTTP_403_FORBIDDEN)

        assignment = get_object_or_404(Assignment, pk=pk)
        if assignment.teacher != request.user:
            return Response({"msg": "Access denied for this assignment"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentSerializer(assignment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Assignment has been updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != UserRole.TEACHER.value:
            return Response({"msg": "Only teachers can delete assignments"}, status=status.HTTP_403_FORBIDDEN)

        assignment = get_object_or_404(Assignment, pk=pk)
        if assignment.teacher != request.user:
            return Response({"msg": "You are not authorized to delete this assignment"}, status=status.HTTP_403_FORBIDDEN)

        assignment.delete()
        return Response({"msg": "Assignment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

from .serializers import StudentAssignmentListSerializer

class StudentAssignmentListApiView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != UserRole.STUDENT.value:
            return Response({"msg": "Only students can access this view."}, status=403)

        assignments = Assignment.objects.filter(
            assigned_class__students=user,
            due_date__gte=timezone.now()
        ).order_by("due_date")

        data = []
        for assignment in assignments:
            serializer = StudentAssignmentListSerializer(assignment)
            has_submitted = AssignmentSubmission.objects.filter(student=user, assignment=assignment).exists()
            data.append({
                **serializer.data,
                "has_submitted": has_submitted
            })

        return Response(data, status=200)

from rest_framework.generics import RetrieveAPIView
from .serializers import StudentAssignmentDetailSerializer

class StudentAssignmentDetailApiView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user

        if user.role != UserRole.STUDENT.value:
            return Response({"msg": "Only students can access this view."}, status=403)

        assignment = get_object_or_404(
            Assignment,
            pk=pk,
            assigned_class__students=user
        )

        serializer = StudentAssignmentDetailSerializer(assignment)

        submission = AssignmentSubmission.objects.filter(student=user, assignment=assignment).first()

        return Response({
            "assignment": serializer.data,
            "has_submitted": submission is not None,
            "submission": {
                "id": submission.id,
                "submitted_at": submission.submitted_at,
                "file_url": submission.file.url if submission and submission.file else None
            } if submission else None
        }, status=200)
