from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Assignment, AssignmentQuestion, AssignmentQuestionThrough
from .forms import AssignmentForm


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

def submit_assignment(request):
    return HttpResponse("Submit Assignment View (placeholder)")
