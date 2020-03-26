from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ClassAverage)
admin.site.register(TotalScore)
admin.site.register(Teacher)
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




