from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ClassAverage)
# admin.site.register(TotalScore)
# admin.site.register(Teacher)
admin.site.register(Term)
admin.site.register(Grade)
admin.site.register(GradeNumber)
admin.site.register(GradeColour)
admin.site.register(Session)
admin.site.register(Subject)
# admin.site.register()
# admin.site.register(Result)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    # readonly_fields = ['total']
    search_fields = ['student__admission_number', 'student__name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['student', 'grade', 'term', 'session', 'subject', 'ca', 'project', 'exam', 'total', 'teacher']
    # defines filter column
    list_filter = ['teacher', 'session', 'term', 'grade', 'subject']
    # defines how the list would be ordered
    ordering = ('session', 'term', 'grade', 'total')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # readonly_fields = ['total']
    # dfeines which fields are searchable
    search_fields = ['name', 'admission_number']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['name', 'admission_number', 'grade', 'birth_date']
    # defines filter column
    list_filter = ['name', 'grade', 'gender']
    # defines how the list would be ordered
    ordering = ('name', 'grade')


@admin.register(TotalScore)
class TotalScoreAdmin(admin.ModelAdmin):
    # readonly_fields = ['total']
    search_fields = ['student__admission_number', 'student__name', 'session__name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['student', 'grade', 'term', 'session', 'total_score', 'average', 'position']
    # defines filter column
    list_filter = ['total_score', 'session', 'term', 'grade', 'position', 'average']
    # # defines how the list would be ordered
    ordering = ('position', 'session', 'term', 'grade', 'total_score')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # readonly_fields = ['total']
    search_fields = ['title', 'name', 'phone']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['title', 'name', 'phone', 'description']
    # defines filter column
    list_filter = ['title', 'name', 'phone']
    # defines how the list would be ordered
    ordering = ('title', 'name')