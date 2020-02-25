from django.db import models
from django.contrib.auth.models import User

class Grade(models.Model):
    '''Defines a class (classroom)'''

    GRADE_CHOICES = (
        ('one', 'one'),
        ('two', 'two'),
        ('three', 'three'),
        ('four', 'four'),
        ('five', 'five'),
        ('six', 'six'),
    )

    # example of name : grade one, grade two
    name = models.CharField(
        max_length=5,
        choices=GRADE_CHOICES,
        default='one'
        )

    GRADE_COLOUR = (
        ('red', 'red'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('white', 'white'),
        ('brown', 'brown'),
    )

    colour = models.CharField(
        max_length=5,
        choices=GRADE_COLOUR,
        default='red'
        )

    def __str__(self):
        return f'{self.name.title()} {self.colour.title()}'
    

class Student(models.Model):
    '''Defines a student'''
    
    name = models.CharField(max_length=250)
    admission_number = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='male'
        )
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} --- {self.admission_number}'


class Teacher(models.Model):
    TITLE_CHOICES = (
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Dr', 'Dr.'),
        ('Madam', 'Madam')
    )
    title = models.CharField(help_text='e.g: Mr. Uche, Mrs. Ngozi', max_length=10, choices=TITLE_CHOICES)
    name = models.CharField(max_length=100, verbose_name='Full Name', help_text='e.g Uche Ngozi')
    phone = models.CharField(null=True, max_length=11, help_text='08012345678')
    description = models.CharField(max_length=250, null=True, blank=True, help_text='Any other info about this teacher')

    def __str__(self):
        if self.title:
            return f'{self.title}. {self.name.title()}'
    

class Subject(models.Model):
    SUBJECT_CHOICES = (
        ('english/verbal', 'English/Verbal'),
        ('spelling', 'Spelling')
    )
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    teacher = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Term(models.Model):
    TERM_CHOICES = (
        ('first', 'first'),
        ('second', 'second'),
        ('third', 'third')
    )

    name = models.CharField(
        max_length=6,
        choices=TERM_CHOICES,
        default='first'
        )

    def __str__(self):
        return self.name


class Session(models.Model):
    SESSION_CHOICES = (
        ('2019/2020', '2019/2020'),
        ('2020/2021', '2020/2021')
    )

    name = models.CharField(
        max_length=9,
        choices=SESSION_CHOICES,
        default='2020/2021'
    )

    def __str__(self):
        return self.name
    

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca = models.PositiveIntegerField(default=0)
    project = models.PositiveIntegerField(default=0)
    exam = models.PositiveIntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.name} --- {self.student.admission_number} --- {self.session.name}'

    

