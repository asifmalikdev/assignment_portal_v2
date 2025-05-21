from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import  FormView
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Assignment, AssignmentQuestionThrough, AssignmentSubmission, StudentAnswer, AssignmentQuestion
from .forms import AssignmentForm, AssignmentSubmissionForm
from .serializers import AssignmentQuestionSerializer, AssignmentSerializer


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
from users.permissions import IsTeacherOrAdmin


class AssignmentQuestionListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,IsTeacherOrAdmin]
    def get(self, request):
        print("Current User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        print("Role:", getattr(request.user, 'role', 'no role'))
        if not request.user:
            return Response({"msg":"we haven't got any user"})

        if request.user.role =="teacher":
            question_book = AssignmentQuestion.objects.filter(teacher = request.user)
        elif request.user.role == "admin":
            question_book = AssignmentQuestion.objects.all()
        else:
            return Response({"msg":"you are not allowed to see this"}, status=403)



        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(question_book, request)


        serializer = AssignmentQuestionSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if request.user.role != "teacher":
            return Response({"msg":"only teacher can post a question"}, status=403)

        serializer = AssignmentQuestionSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(teacher = request.user)
            return Response({"msg", "new question is added"}, status=201)
        return Response(serializer.errors)


class AssignmentQuestionDetailAPIView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(AssignmentQuestion, pk=pk)
    def get(self,request, pk):
        question=self.get_object(pk)
        if not question:
            return Response({"msg":"question not found "}, status=404)
        serializer = AssignmentQuestionSerializer(question)
        return Response(serializer.data)
    def put(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"msg":"can't find question to update"}, status=404)
        if question.teacher != request.user:
            return Response({"msg":"this teacher is not allowed to update"})
        serializer = AssignmentQuestionSerializer(question, data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"data is updated in db"})
        return Response(serializer.error)

    def delete(self, request, pk):
        question = self.get_object(pk)
        if question.teacher != request.user:
            return Response({"msg":"this teacher cannot delete"}, status=404)
        question.delete()
        return Response({"msg":"question is deleted"})

class AssignmentListCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        user_now = request.user
        if user_now.role == 'teacher':
            assignments = Assignment.objects.filter(teacher = user_now)
        elif user_now.role == "admin":
            assignments = Assignment.objects.all()
        else:
            return Response({"msg":"You are not authenticated to see the assignments"}, 403)


        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(assignments, request)

        serializer = AssignmentSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        if not request.user:
            return Response({"msg":"who are you buddy"})
        if request.user.role != 'teacher':
            return Response({"You are not allowed to create assignment"}, status=403)

        serializer = AssignmentSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(teacher = request.user)
            return Response({"msg":"assignment has been created"}, status=201)
        return Response(serializer.errors)

class AssignmentDetailView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes=[IsAuthenticated, IsTeacherOrAdmin]

    def get_object(self, pk):
        return get_object_or_404(Assignment, pk=pk)

    def get(self, request, pk):
        print(request.user)
        id = pk
        assignment = self.get_object(id)
        if assignment.teacher != request.user:
            return Response({"msg":"Access Denied for this teacher"}, status=403)
        if not assignment:
            return Response({"msg":"No Assignment with this Id"}, status=403)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)
    def put(self, request, pk):
        if not request.user:
            return Response({"msg":"Who are you buddy"})
        if request.user.role != 'teacher':
            return Response({"msg":"You are not authenticate to Update this assignment"})

        id = pk
        assignment = self.get_object(id)
        if not assignment:
            return Response({"could not find assignmet"})

        serializer = AssignmentSerializer(assignment, data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Assignment has been updated"}, status=200)
        return Response(serializer.errors)
    def delete(self, request, pk):
        if not request.user:
            return Response({"msg":"User Required"}, status = 403)
        if request.user.role != "teacher":
            return Response({"msg":"Only Teacher can perform delete operations"}, status=403)
        id = pk
        assignment = self.get_object(id)
        if not assignment:
            return Response({"msg":"We could not find any assignment"}, status=404)

        if assignment.teacher != request.user:
            return Response({"You are not authorised to delete this assignment"}, status = 403)

        assignment.delete()
        return Response({"msg":"Record Delted"}, status=204)





