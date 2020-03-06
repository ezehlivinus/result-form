from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class GradeNumber(models.Model):
    NUMBER_CHOICES = (
        ('one', 'one'),
        ('two', 'two'),
        ('three', 'three'),
        ('four', 'four'),
        ('five', 'five'),
        ('six', 'six')
    )

    name = models.CharField(
        max_length=10,
        choices=NUMBER_CHOICES,
        default='one',
        unique=True
        )

    def __str__(self):
        return self.name


class GradeColour(models.Model):
    
    COLOUR_CHOICES = (
        ('green', 'green'),
        ('red', 'red'),
        ('blue', 'blue'),
        ('white', 'white'),
        ('yellow', 'yellow'),
        ('purple', 'purple'),
    )

    name = models.CharField(default='green', max_length=50, choices=COLOUR_CHOICES, unique=True)
    
    def __str__(self):
        return self.name 
    

class Grade(models.Model):
    '''Defines a class (classroom)'''
    number = models.ForeignKey(GradeNumber, on_delete=models.CASCADE)
    colour = models.ForeignKey(GradeColour, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        'Teacher', 
        verbose_name='Grade Teacher',
        on_delete=models.CASCADE,
        help_text='This is the class teacher for this grade')

    def __str__(self):
        return f'{self.number} {self.colour}'
    

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
        ('spelling', 'Spelling'),
        ('Basic Science', 'Basic Science'),
        ('Physics', 'Physics'),
    )
    is_offered_by_junior = models.BooleanField(default=True, help_text='Is this subject also offered by junior pupils: in grade 1 - 3?')
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES, unique=True, verbose_name='Title')
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
    # def validate_min(self, value):
    #     if value < 0:
    #         raise ValidationError(message='The value must be less than 30',

    #     )
    def validate_max(self, value):
        if value > 100:
            raise ValidationError(message='The value must be greater ',

        )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca = models.PositiveIntegerField(default=0)
    project = models.PositiveIntegerField(default=0)
    exam = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    comment = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.name} --- {self.student.admission_number} --- {self.session.name}'

    def save(self, *args, **kwargs):
        self.total = self.ca + self.project + self.exam
        super(Result, self).save(*args, **kwargs)

