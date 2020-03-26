from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from.forms import StudentForm
from django.http import HttpResponseRedirect


from django.http import HttpResponse
from django.views.generic import View


from result.helpers import *

from .all_views.positions import position

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
        [results, student, session, term, grade, total_score, class_average, comments] = student_result(request, pk)

        context = {
            'student': student,
            'session': session,
            'grade': grade,
            'term': term,
            'results': results,
            'total_score': total_score,
            'pupil_average': round(total_score.average, 3),
            'class_average': class_average,
            'comments': comments,
        }

        template_name = 'result/student_result.html'
        return render(request, template_name, context)

def student_result(request, pk):
    '''Return student results'''
    session_id  = request.POST['session']
    grade_id = int(request.POST['grade'])
    admin_number = int(request.POST['admin_number'])

    term = get_object_or_404(Term, pk=int(request.POST['term']))
    session = get_object_or_404(Session, pk=session_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    student = get_object_or_404(Student, pk=pk, admission_number=admin_number)
    # results = get_object_or_404(Result, student=student, session=session_id, grade=grade_id)
    results = Result.objects.all().filter(student=student, session=session_id, grade=grade_id, term=int(request.POST['term']) )
    # if results does not exist, 
    if not results.exists():
        raise Exception({'error': f'{results} No result for this pupil in this grade, session or term'})

    try:
        total_score = TotalScore.objects.get(
            student_id=student.id,
            term_id=term.id, 
            session_id=session.id, 
            grade_id=grade.id
        )

        class_average = ClassAverage.objects.get(
            term_id=term.id, 
            session_id=session.id, 
            grade_id=grade.id
        )

        comments = term_comments()
    except:
        raise

    return [results, student, session, term, grade, total_score, class_average, comments]


def edit(request, pk):
    '''Allow user to edit student result under POST request only for now'''

    if request.method == 'GET':
        return redirect('detail', pk = pk)
        # return render(request, 'result/edit_result.html', context={'grade': 'GET MEthods'})

    admin_number = int(request.POST['admin_number'])
    student = get_object_or_404(Student, pk=pk, admission_number=admin_number)
    session_id = int(request.POST['session'])
    session = get_object_or_404(Session, pk=session_id)
    term = get_object_or_404(Term, pk=int(request.POST['term']))
    grade = get_object_or_404(Grade, pk=int(request.POST['grade']))

    if is_junior(grade.number.name):
        # Get only the subjects offered by junior pupils
        subjects = Subject.objects.filter(is_offered_by_junior=True)
        # to get the result that has been submitted already
        results = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        ).filter(subject__is_offered_by_junior=True)


    else:
        # === to above
        subjects = Subject.objects.all()
        results = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        subject=subjects
        )
        

    # use in determining which subject that has been submitted to the result table
    submitted_subjects = []
    sum_of_totals = 0
    for result in results:
        submitted_subjects.append(result.subject.id )
        sum_of_totals += result.total        

    # get student total score
    total_score = TotalScore.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
    )

    if total_score.exists():
        # we want to update it
        total_score = total_score[0]
            
        total_score.total_score = sum_of_totals
        total_score.average = sum_of_totals / subjects.count()
        total_score.term = term
        total_score.session = session
        total_score.grade = grade
        total_score.student = student

        total_score.save()

    else:
        # we want to create a new record in total_score table/models
        try:
            total_score = TotalScore(
                total_score = sum_of_totals,
                average = sum_of_totals / subjects.count(),
                term = term,
                session = session,
                grade = grade,
                student = student
            )
            
            total_score.save()
            
        except:
            raise


    comments = term_comments()

    context = {
        'term': term,
        'grade': grade,
        'subjects': subjects,
        'session': session,
        'comments': comments,
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
    
   
    # check if the session, term, grade, submit has existed for this student
    result = Result.objects.filter(
        student=student,
        grade=grade,
        term=term,
        session=session,
        subject=subject
        )
    
    

    ca = int(request.POST['ca'])
    project = int(request.POST['project'])
    exam = int(request.POST['exam'])

    teacher = get_object_or_404(Teacher, pk=int(request.POST['teacher']))
    
    if result.exists():
        # try updating the result instead of throwing an error with message=Result already exist
        # access the object in the queryset
        result = result[0]

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

        result.save() # total is calculated on the model
    else:
    # if not, create new result
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
    

def compute_class_average(request, pk):
    # This has being rewritten at all_views.positions.position.py
    pass


# Below was intend and used for simulating generating pdf result
# for now it we are using JS method: windows.print()
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

