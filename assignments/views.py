from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Assignment, AssignmentQuestion, AssignmentQuestionThrough, AssignmentSubmission, StudentAnswer
from .forms import AssignmentForm, AssignmentSubmissionForm
from django.utils import timezone

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
        context["question_book"]=AssignmentQuestion.objects.filter(teacher = self.request.user)
        return context
    def form_valid(self, form):
        assignment=form.save(commit=False)
        assignment.teacher = self.request.user
        assignment.save()
        selected_question_ids = self.request.POST.getlist("questions")
        for order, qid in enumerate(selected_question_ids):
            AssignmentQuestionThrough.objects.create(
                assignment = assignment,
                question_id=qid,
                order = order
            )
        return super().form_valid(form)

from django.views import View

class StudentAssignment(View):
    template_name="student_assignment.html"
    def get(self, request):

        return render(request, self.template_name)
from django.views.generic import ListView
from .models import Assignment
from django.utils import timezone

class StudentAssignmentListView(ListView):
    model = Assignment
    template_name = 'student_assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        user = self.request.user
        # Only show assignments for classes the student is enrolled in & before due date
        return Assignment.objects.filter(
            assigned_class__students=user,
            due_date__gte=timezone.now()
        ).order_by('due_date')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return HttpResponse("You are not allowed to view this page.")
        return super().dispatch(request, *args, **kwargs)








class AssignmentSubmitView(View):
    template_name = "submit_assignment.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return HttpResponseForbidden("You are not allowed to access this page")
        return super().dispatch(request, *args, **kwargs)



    def get_assignment(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id = assignment_id)
        if not assignment.assigned_class.students.filter(id=request.user.id).exists():
            return None
        return assignment
    def get(self, request, assignment_id):
        assignment = self.get_assignment(request, assignment_id)
        if not assignment:
            return HttpResponseForbidden("you are not enroled in this class")
        if AssignmentSubmission.objects.filter(student=request.user, assignment= assignment).exists():
            return HttpResponse("you have alrady submitted this assignment")
        form = AssignmentSubmissionForm(assignment=assignment)
        return render(request, self.template_name, {'form': form, 'assignment': assignment})

    def post(self, request, assignment_id):
        assignment = self.get_assignment(request, assignment_id)
        if not assignment:
            return HttpResponseForbidden("You are not enrolled in this class.")
        if assignment.due_date < timezone.now():
            return HttpResponse("Submission deadline has passed")
        if AssignmentSubmission.objects.filter(student=request.user, assignment= assignment):
            return HttpResponse("you have already submitted this assignment")
        form = AssignmentSubmissionForm(request.POST, assignment= assignment)
        if form.is_valid():
            submission = AssignmentSubmission.objects.create(
                student = request.user,
                assignment=assignment
            )
            for question in assignment.questions.all():
                answer_value = form.cleaned_data.get(f"question_{question.id}")
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    answer_text=answer_value if question.question_type != 'MCQ' else None,
                    selected_option=answer_value if question.question_type == 'MCQ' else None
                )
            messages.success(request, "Your assignment was submitted successfully.")
            return redirect('student_dashboard')
        return render(request, self.template_name, {'form': form, 'assignment': assignment})




def submit_assignment(request):
    return HttpResponse("Submit Assignment View (placeholder)")
