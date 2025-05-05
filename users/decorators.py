from django.contrib.auth.decorators import user_passes_test

def teacher_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_authenticated and u.role == "teacher")(view_func)
    return decorated_view_func

def student_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_authenticated and u.role == "student")(view_func)
    return decorated_view_func

def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.role == 'admin'))(view_func)
    return decorated_view_func
