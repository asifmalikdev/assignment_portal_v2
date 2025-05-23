from django.contrib import admin
from .models import District, School, ClassRoom
from .forms import ClassForm

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('create_time',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','address', 'district', 'created_at', 'is_active')
    list_filter = ('district', 'is_active', 'name', 'id')
    search_fields = ('name', 'district__name',)
    ordering = ('created_at',)
    list_display_links = ('name',)

@admin.register(ClassRoom)
class ClassAdmin(admin.ModelAdmin):
    form = ClassForm
    list_display = ('id', 'name', 'grade_level', 'school', 'is_active', 'assigned_teacher', 'students_list', )
    list_filter = ('grade_level', 'school', 'is_active')
    ordering = ('created_at',)
    def students_list(self, obj):
        students = obj.students.all()
        if not students:
            return "no students yet"
        return " , ".join([stu.get_full_name() for stu in students])

    students_list.short_description = "Students"

