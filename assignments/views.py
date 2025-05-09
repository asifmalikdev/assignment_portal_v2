from django.http import HttpResponse
from django.shortcuts import render

from assignments.models import AssignmentQuestion


def assignment_create_view(request):
    print(request.user.full_name)
    question_book = AssignmentQuestion.objects.filter(teacher=request.user)

    print("printing query set",question_book, type(question_book))


    context = {
        'question_book':question_book,
    }
    return render(request, "assignment_create_template.html", context)

def submit_assignment(request):
    return HttpResponse("Submit Assignment View (placeholder)")
