def term_comments():
    '''Returns term comments'''
    term_comments = {
        1: 'Consistently good worker',
        2: 'Participates actively in class',
        3: 'Completes works on time',
        4: 'Shows talent',
        5: 'Reads fluently',
        6: 'Memorizes well',
        7: 'Enjoys this subject',
        8: 'Does good work',
        9: 'Does good work',
        10: 'A slow worker, but tries',
        11: 'Is improving',
        12: 'Finds this subject diff.',
        13: 'Could do better if he/she tries',
        14: 'Does not complete work',
        15: 'Needs constant pressure',
        16: 'Slow reader, daily practice neccessary',
        17: 'Memory work poor',
        18: 'Careless and untidy',
        19: 'An untidy worker',
        20: 'Shows little interest',
        21: 'Needs special attention',
        22: 'Homework unsatisfy needs supervisor'


    }

    return term_comments

def is_junior(grade_number):
    '''Check if this grade is junior grader or not'''
    junior = ['one', 'two', 'three']
    # senior = ['four', 'five', 'six']
    if grade_number in junior:
        return True
    return False

