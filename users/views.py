from django.contrib.auth import login, logout
from django.http import  HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from school.models import District, School, ClassRoom
from school.forms import DistrictForm, SchoolForm, ClassForm
from users.decorators import teacher_required, student_required, admin_required
from users.forms import UserLoginForm, TeacherSignupForm, StudentSignupForm, AdminSignupForm
from django.contrib.auth import authenticate
from assignments.models import Assignment, AssignmentQuestion, AssignmentQuestionThrough
from assignments.forms import AssignmentForm, AssignmentQuestionThroughForm, AssignmentQuestionInLineForm


def validate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
        return user
    else:
        return None

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = validate_user(email, password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher' or user.is_superuser:
                return redirect('teacher_dashboard')
            elif user.role == 'student' or user.is_superuser:
                return redirect('student_dashboard')
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_admin(request):
    if request.method == 'POST':
        form  = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = AdminSignupForm
        return render(request, 'signup.html', {'form': form, 'role':'Admin'})


def signup_teacher(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = TeacherSignupForm()
    return render(request, 'signup.html', {'form': form, 'role':'Teacher'})

def signup_student(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StudentSignupForm()

    return render(request, 'signup.html',{'form': form, 'role':'Student'})




def teacher_basic_info(request):
    role_is = request.user.role
    name_is = request.user.full_name
    email_is = request.user.email
    all_classes_of_teacher = ClassRoom.objects.filter(assigned_teacher__email__iexact=email_is)
    temp = 0
    for class_ in all_classes_of_teacher:
        temp += 1
    return name_is, email_is, temp

@method_decorator(teacher_required, name='dispatch')
class TeacherDashboardView(View):
    template_name = 'teacher_dashboard.html'

    def get(self, request):
        if request.user.role !='teacher':
            return HttpResponse("this moduel is only for teacher")
        name_is, email_is, temp = teacher_basic_info(request)


        class_filter = request.GET.get('class_id')
        classes = request.user.teaching_classes.all()

        if class_filter:
            questions = AssignmentQuestion.objects.filter(teacher = request.user, assigned_class__id = class_filter)
            assignments = Assignment.objects.filter(teacher = request.user, assigned_class__id = class_filter)
        else:
            questions = AssignmentQuestion.objects.filter(teacher = request.user)
            assignments = Assignment.objects.filter(teacher=request.user)

        question_forms = {
            q.id: AssignmentQuestionInLineForm(instance=q, user=request.user)
            for q in questions
        }

        context = {
            'classes': classes,
            'selected_class_id':class_filter,
            "assignment_form": AssignmentForm(request = request),
            "question_form":AssignmentQuestionInLineForm(user=request.user),
            'question_forms' : question_forms,
            'assignments' : assignments,
            'questions': questions,
            "name_is": name_is,
            "email_is": email_is,
            'total_classes': temp
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'create_question':
            form = AssignmentQuestionInLineForm(request.POST, user=request.user)
            if form.is_valid():
                question = form.save(commit=False)
                question.teacher = request.user
                question.save()
                messages.success(request, "Question created successfully.")
            else:
                messages.error(request, "Error creating question.")



        elif action == 'edit_question':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(AssignmentQuestion, id=question_id, teacher=request.user)
            form = AssignmentQuestionInLineForm(request.POST, instance=question, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Question updated.")

            else:

                messages.error(request, "Error updating question.")


        elif action == 'delete_question':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(AssignmentQuestion, id=question_id, teacher=request.user)
            question.delete()
            messages.success(request, "Question deleted.")

        elif action == 'create_assignment':
            form = AssignmentForm(request.POST, request=request)
            if form.is_valid():
                assignment = form.save()
                messages.success(request, "Assignment created.")
            else:
                messages.error(request, "Error creating assignment.")


        elif action == 'edit_assignment':
            assignment = get_object_or_404(Assignment, id=request.POST.get('assignment_id'), teacher=request.user)
            form = AssignmentForm(request.POST, instance=assignment, request=request)
            if form.is_valid():
                form.save()
                messages.success(request, "Assignment updated.")
            else:
                messages.error(request, "Error updating assignment.")


        elif action == 'delete_assignment':
            assignment_id = request.POST.get('assignment_id')
            assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
            assignment.delete()
            messages.success(request, "Assignment deleted.")

        return redirect('teacher_dashboard')

def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    assignment.delete()
    messages.success(request, 'Assignment deleted.')
    return redirect('teacher_dashboard')
def delete_question(request, pk):
    question = get_object_or_404(AssignmentQuestion, pk=pk, teacher=request.user)
    question.delete()
    messages.success(request, 'Question deleted.')
    return redirect('teacher_dashboard')




@student_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')
@admin_required
def admin_dashboard(request):
    districts = District.objects.all()
    schools = School.objects.all()
    classes = ClassRoom.objects.all()
    district_form = DistrictForm()
    school_form = SchoolForm()
    class_form = ClassForm()
    district_search_query = request.GET.get('district_search')
    if district_search_query:
        districts = districts.filter(name__icontain=district_search_query)
    school_search_query = request.GET.get('school_search')
    if school_search_query:
        schools = schools.filter(name__icontain = school_search_query)

    class_search_query = request.GET.get('class_search')
    if class_search_query:
        classes = classes.filter(name__icontain = class_search_query)

    selected_district_id = request.GET.get('district_id')
    if selected_district_id:
        schools = schools.filter(district_id = selected_district_id)

    if request.method == 'POST' and 'add_district' in request.POST:
        district_form = DistrictForm(request.POST)
        if district_form.is_valid():
            district_form.save()
            return redirect('admin_dashboard')
    if request.method == 'POST' and 'add_school' in request.POST:
        school_form = SchoolForm(request.POST)
        if school_form:
            school_form.save()
            return redirect('admin_dashboard')
    selected_school_id = request.GET.get('school_id')
    if selected_school_id:
        classes = classes.filter(school_id = selected_school_id)
    if request.method == 'POST' and 'add_class' in request.POST:
        class_form = ClassForm(request.POST)
        if class_form.is_valid():
            class_form.save()
            return redirect('admin_dashboard')




    context = {
        'districts': districts,
        'schools': schools,
        'district_form':district_form,
        'school_form': school_form,
        'selected_district_id':selected_district_id,
        'classes': classes,
        'class_form': class_form,
        'selected_school_id': selected_school_id
    }
    return render(request, 'admin_dashboard.html', context)


def delete_district(request, district_id):
    district = get_object_or_404(District, id=district_id)
    district.delete()
    return redirect('admin_dashboard')
def delete_school(request, school_id):
    school = get_object_or_404(School, id = school_id)
    school.delete()
    return redirect('admin_dashboard')

def delete_class(request, classroom_id):
    class_ = get_object_or_404(ClassRoom, id = classroom_id)
    class_.delete()
    return redirect('admin_dashboard')
