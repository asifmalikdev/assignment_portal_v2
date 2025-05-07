from django.http import HttpResponse

def assignment_create_view(request):
    print(request.user.full_name)
    return HttpResponse("Create Assignment View (placeholder)")

def submit_assignment(request):
    return HttpResponse("Submit Assignment View (placeholder)")
