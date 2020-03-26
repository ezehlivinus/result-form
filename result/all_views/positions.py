from result.models import ClassAverage, Grade, Session, Term, TotalScore
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect, HttpResponseNotFound
import pandas as pd
from num2words import num2words


def position(request):
    
    sessions = Session.objects.all()
    terms = Term.objects.all()
    grades = Grade.objects.all()
    
    # For rendering the template
    if request.method == 'GET':
        
        context = {
            'sessions': sessions,
            'grades': grades,
            'terms': terms,
        }

        return render(request, 'result/positions.html', context)
    
    # Here handles POST request

    # handles submitted/form data
    grade_id = request.POST.get('grade', False)
    session_id = request.POST.get('session', False)
    term_id = request.POST.get('term', False)

    if grade_id and session_id and term_id:
        [grade, session, term, total_scores] = get_total_score(grade_id, session_id, term_id)

        number_in_class = request.POST.get('number_in_class', False)
        if number_in_class:
            # we want to compute class average
            try:
                # we want to update
                class_average = ClassAverage.objects.get(
                    grade_id = grade.id,
                    session_id = session.id,
                    term_id = term.id
                )
                # without casting total_scores to list()
                # if the queryset is one, it iterate may raise not iterable exception if attempt is made
                average = compute_class_average(list(total_scores))

                class_average.number_of_score = total_scores.count()
                class_average.number_in_class = number_in_class
                class_average.average = average

                class_average.save()

            except ClassAverage.DoesNotExist:
                # we want to create new class average

                # we casted total_scores to list() type to enable 
                # us iterate if the queryset return only one row
                average = compute_class_average(list(total_scores))
                class_average = ClassAverage(
                    number_of_score = total_scores.count(),
                    number_in_class = number_in_class,
                    average = average,
                    session = session,
                    grade = grade,
                    term = term
                )

                class_average.save()
            except:
                # if something else happens during computation of class average
                raise

            # # compute the students positions
            # positions = compute_positions(list(total_scores))
            # # Write positions for each students into database (total_score table)
            # students = save_positions(positions, total_scores)

        # we still want to compute students' positions anyway and save
        positions = compute_positions(list(total_scores))
        students = save_positions(positions, total_scores)
        
        class_average = get_class_average(grade, session, term)
        
        if len(students):
            context = {
                'positions': students,
                'class_average': class_average[0],
                'grades': Grade.objects.all(),
                'sessions': Session.objects.all(),
                'terms': Term.objects.all(),
                'class_average_exist': class_average.count()

            }
            return render(request, 'result/positions.html', context)

        raise Exception({'valueOrObjectError': students })
    else:
        raise Exception({'valueError': 'Grade, Seesion or Term cannot be empty'})

def save_positions(positions, total_score_objs):
    '''
    This saves/update students' positions
    @param: positions -> {key: value, ...}, total_score_objs -> query_set
    @return a list of students with their position already saved as an objects/queryset: [student, ...] 
    '''
    # List of students whose positions has been saved
    students = []
    try:
        for student_id, position in positions.items():
            # from this existing queryset filter this student
            this_student = total_score_objs.filter(student=student_id)[0]
            setattr(this_student, 'position', position)
            # this_student.position = position # works and same as above
            students.append(this_student)

        TotalScore.objects.bulk_update(students, ['position'])
        
    except:
        raise
    
    return students 

def get_total_score(grade_id, session_id, term_id ):
    '''Gets total score for the given session, term, grade'''
    grade = get_object_or_404(Grade, pk=grade_id)
    session = get_object_or_404(Session, pk=session_id)
    term = get_object_or_404(Term, pk=term_id)

    total_scores = TotalScore.objects.filter(
        session = session,
        term = term,
        grade = grade
    )
    
    if total_scores.exists():
        return [grade, session, term, total_scores]
    raise Http404({'Some info': f'{total_scores}, model {TotalScore}'})

def get_class_average(grade, session, term):
    class_average = ClassAverage.objects.filter(
        session = session,
        term = term,
        grade = grade
    )

    return class_average

def compute_class_average(total_score_obj):
    '''Compute and return the average scores for this class/grade'''
    try:
        list_of_score = []
        for obj in total_score_obj:
            list_of_score.append(obj.total_score)
        average = sum(list_of_score) / len(list_of_score)

    except:
        raise

    return average


def compute_positions(total_score_obj):
    '''Transforms and returns ranks into positions in order of: 1st, 2nd,....'''
    
    ranks = compute_rank(total_score_obj)

    positions = {}
    try:
        for student_id, student_rank in ranks.items():
            position = num2words(int(student_rank), to='ordinal_num')
            positions.update({student_id: position})
    except:
        raise
    
    # return {student_id: 1st, student_id: 2nd, ...}
    return positions


def compute_rank(total_score_obj):
    '''
    @Param: total_score_onj is an object holding list of students scores
    Return a dictionary of ranked student scores in key/value==student_id/ranks
    '''
    scores = []
    students_id = []
    try:
        for obj in total_score_obj:
            students_id.append(obj.student.id)
            scores.append(obj.total_score)

        series = pd.Series(scores)
        series.index = students_id

        # ascending = False means that the max number should take first rank, min number takes the first
        # a series as this [5, 10, 7, 5] should yield 3.5, 1.0, 2.0, 3.5 otherwise 1.5, 4.0, 2.0, 1.5 
        ranks = series.rank(ascending=False)
    except:
        raise
    
    # return {student_id: rank, student_id: rank, ...}
    return dict(ranks)

