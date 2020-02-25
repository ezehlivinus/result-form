from django.shortcuts import render, get_object_or_404
from .models import *
from.forms import StudentForm
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = StudentForm
        return render(request, 'result/index.html', {'form': form })
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            admin_number = form.cleaned_data['admission_number']
            student = get_object_or_404(Student, admission_number=admin_number)
            
            return HttpResponseRedirect(f'/result/students/{student.id}/')

def detail(request, pk):
    if request.method == 'GET':
        student = get_object_or_404(Student, pk=pk)
        # result = get_object_or_404(Student, admission_number=admin_number)
        sessions = Session.objects.all()
        grades = Grade.objects.all()
        context = {
            'student': student,
            'sessions': sessions,
            'grades': grades
        }

        template_name = 'result/student_detail.html'
        return render(request, template_name, context)
    if request.method == 'POST':
        session_id  = request.POST['session']
        grade_id = int(request.POST['grade'])
        context = {
            'session': session_id,
            'grade': grade_id
        }
        template_name = 'result/student_result.html'
        return render(request, template_name, context)

def result(request):
    pass