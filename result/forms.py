from result.models import Student
from django import forms

class StudentForm(forms.Form):
    
    admission_number = forms.CharField(max_length=10, label='')
    admission_number.widget.attrs.update({'class': 'form-control', 'placeholder': 'Admission Number: 1234'})


