from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
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
    readonly_fields = ['total']





