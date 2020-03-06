from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from.forms import StudentForm
from django.http import HttpResponseRedirect


from django.http import HttpResponse
from django.views.generic import View


from result.helpers import *


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
    # To get student detail
    if request.method == 'GET':
        student = get_object_or_404(Student, pk=pk)
        # result = get_object_or_404(Student, admission_number=admin_number)
        sessions = Session.objects.all()
        grades = Grade.objects.all().order_by('number') 
        terms = Term.objects.all()
        context = {
            'student': student,
            'sessions': sessions,
            'grades': grades,
            'terms': terms
        }

        template_name = 'result/student_detail.html'
        return render(request, template_name, context)
    if request.method == 'POST':
        # Get this student's result
        [results, student, session, term, grade] = student_result(request, pk)

        total_score = 0
        for result in results:
            total_score += result.total


        context = {
            'student': student,
            # 'subject': results.subject,
            'session': session,
            'grade': grade,
            # 'teacher': results.teacher,
            'term': term,
            'results': results,
            'total_score': total_score,
            'pupil_average': total_score / results.count()

        }

        template_name = 'result/student_result.html'
        return render(request, template_name, context)

def student_result(request, pk):
    session_id  = request.POST['session']
    grade_id = int(request.POST['grade'])
    admin_number = int(request.POST['admin_number'])

    term = get_object_or_404(Term, pk=int(request.POST['term']))
    session = get_object_or_404(Session, pk=session_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    student = get_object_or_404(Student, pk=pk, admission_number=admin_number)
    # results = get_object_or_404(Result, student=student, session=session_id, grade=grade_id)
    results = Result.objects.all().filter(student=student, session=session_id, grade=grade_id, term=int(request.POST['term']) )
    
    return [results, student, session, term, grade]


def edit(request, pk):
    if request.method == 'GET':
        return render(request, 'result/edit_result.html', context={'grade': 'GET MEthods'})

    admin_number = int(request.POST['admin_number'])
    student = get_object_or_404(Student, pk=pk, admission_number=admin_number)
    session_id = int(request.POST['session'])
    session = get_object_or_404(Session, pk=session_id)
    term = get_object_or_404(Term, pk=int(request.POST['term']))
    grade = get_object_or_404(Grade, pk=int(request.POST['grade']))

    if is_junior(grade.number.name):
        # Get only the subjects offered by junior pupils
        subjects = Subject.objects.filter(is_offered_by_junior=True)
        results = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        ).filter(subject__is_offered_by_junior=True)


    else:
        subjects = Subject.objects.all()
        results = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        subject=subjects
        )
        
    submitted_subjects = []
    
    for result in results:
        submitted_subjects.append(result.subject.id )

    terms_comments = term_comments()

    context = {
        'term': term,
        'grade': grade,
        'subjects': subjects,
        'session': session,
        'comments': terms_comments,
        'student': student,
        'results': results,
        'submitted_subjects': submitted_subjects,
        
    }
    return render(request, 'result/edit_result.html', context)


def submit_result(request, pk, subject_id):
    

    student = get_object_or_404(Student, pk=pk)
    session_id = int(request.POST['session'])
    session = get_object_or_404(Session, pk=session_id)
    term = get_object_or_404(Term, pk=int(request.POST['term']))
    grade = get_object_or_404(Grade, pk=int(request.POST['grade']))
    subject = get_object_or_404(Subject, pk=subject_id )
    comment = int(request.POST['comment'])
    
   
    # check if the session, term, grade, submit has exited for this student
    result = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        subject=subject
        )
    
    already_exist = True if result.count() else False

    ca = int(request.POST['ca'])
    project = int(request.POST['project'])
    exam = int(request.POST['exam'])

    teacher = get_object_or_404(Teacher, pk=int(request.POST['teacher']))

    if already_exist:
        # if it doest exist
        # try updating the result instead of throwing an error with message=Result already exist
        result = Result.objects.get(
        student_id=student.id,
        grade_id=grade.id,
        term_id=term.id,
        session_id=session.id,
        subject_id=subject.id
        )

        result.student=student
        result.grade=grade
        result.term=term
        result.session=session
        result.subject=subject
        result.comment=comment
        result.ca=ca
        result.project=project
        result.exam=exam
        result.teacher=teacher

        result.save()

        # return render(request, 'result/edit_result.html', context={'result': result } )
    else:
    # create new result
        result = Result(
            student=student,
            grade=grade,
            term=term,
            session=session,
            subject=subject,
            comment=comment,
            ca=ca,
            project=project,
            exam=exam,
            teacher=teacher
        )

        result.save()

    return edit(request, pk)
    return render(request, 'result/edit_result.html', context={'result': result } )



import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.template import Context


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }

        # return render(request, 'result/invoice.html', context=data)
        filename = "Invoice_%s.pdf" %("12341231")
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "inline; filename=invoive-123445.pdf"
        template = get_template('result/student_result.html')
        html = template.render(data)

        pisa_status = pisa.CreatePDF(
            html, dest=response,
        )
        if pisa_status.err:
            return HttpResponse('Error......')
        return response

