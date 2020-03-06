def term_comments():
    '''Returns term comment'''
    term_comments = {
        1: 'Consistently', 2: 'Participates actively in class', 3: 'Completes works on time',
        4: 'Shows talents', 5: 'Reads fluently'
    }

    return term_comments

def is_junior(grade_number):
    '''Check if this grade is junior grader or not'''
    junior = ['one', 'two', 'three']
    senior = ['four', 'five', 'six']
    if grade_number in junior:
        return True
    return False
