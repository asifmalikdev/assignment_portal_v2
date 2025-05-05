from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, get_object_or_404
from users.decorators import teacher_required, student_required, admin_required
from users.forms import UserLoginForm, TeacherSignupForm, StudentSignupForm, AdminSignupForm
from django.contrib.auth import authenticate

def validate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
        return user
    else:
        return None

def login_view(request):
    if request.method == 'POST':
        print('hello asif he')
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


from school.models import District, School, ClassRoom
from school.forms import DistrictForm, SchoolForm, ClassForm


@teacher_required
def teacher_dashboard(request):

    return render(request, 'teacher_dashboard.html')

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
    class_from = ClassForm
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
        'class_from': class_from,
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
