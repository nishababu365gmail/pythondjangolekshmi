from django import forms
from django.core.exceptions import ValidationError
from django.forms.forms import Form
from django.shortcuts import render
import re
from lekshmiapp.models import(Employee,student,
course,studentcourse,State,City) 
from django.forms import ModelForm
from django_select2 import forms as select2forms
class rdbuttonform(forms.Form):
    status=forms.BooleanField(widget=forms.RadioSelect(choices=[(1,'y'),(2,'N')]))
class statemodelform(ModelForm):
    class Meta:
        model=State
        fields='__all__'
class citymodelform(ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        mychoices=State.objects.all()        
        self.fields["state"]=forms.ModelChoiceField(queryset=mychoices,widget=select2forms.Select2Widget(attrs={'class':'select2'}))
    class Meta:
        model=City
        fields=['city_name','state']


class studentmodelform(ModelForm):
    def __init__(self, *args, **kwargs):
        crs=course.objects.all().values_list('course_id','course_name')
        
        super().__init__(*args, **kwargs)
        self.fields["student_courses"]=forms.ModelMultipleChoiceField(queryset=course.objects.all(),widget=forms.SelectMultiple(attrs={'width':'50px','class':'select2','multiple':'multiple'}))
        self.fields["student_date_of_birth"]=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    class Meta:
        model=student
        exclude=['student_id']

class simpleinputform(forms.Form):
    fname = forms.CharField(max_length=100, label="Enter first Name")
    lname = forms.CharField(max_length=100, label="Enter second Name")
    adharno = forms.CharField(max_length=100, label="Enter adhar No")
    age = forms.IntegerField(label="Enter age")


class EmployeeModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee_fname"].widget.attrs.update(size='40')
        self.fields["employee_lname"]=forms.CharField(widget=forms.TextInput(attrs={'data-modelname': 'employee','data-fieldname': 'employee_lname','class':'duplicatecheck'}))
        self.fields["employee_adharnos"]=forms.CharField(widget=forms.TextInput(attrs={'data-modelname': 'employee','data-fieldname': 'employee_adharnos','class':'duplicatecheck'}))
    class Meta:
        model = Employee
        fields = [
            "employee_fname",
            "employee_lname",
            "employee_adharnos",
            "employee_age",
            "employee_state",
            
            # "employee_city",
        ]
        widgets = {            
            'employee_fname': forms.TextInput(attrs={'id': 'bod',  'required': True, 'placeholder': 'hiii'}
            ),}
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["employee_state"].widget.attrs.update(size="40")
BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

class SimpleForm(forms.Form):
    birthdate = forms.DateField(
        label=('Birthdate'),
        widget=forms.DateInput(
            attrs={'placeholder': '__/__/____', 'class': 'date',}))
  #birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
        
    )
    gender=forms.BooleanField(widget=forms.RadioSelect(choices=FAVORITE_COLORS_CHOICES),label="Gender"
        
    )
def isPasswordMatch(firstone,secondone):
    return firstone==secondone
def validate_hash(value):
    reg = re.compile('^[#](\w+)$')
    if not reg.match(value) :
        #raise ValidationError(u'%s hashtag doesnot comply' % value)
        raise ValidationError(f'{value} hashtag doesnot comply')
class testcustomsvalidators(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput())
    repassword=forms.CharField(widget=forms.PasswordInput())
    hashfield=forms.CharField(max_length=10,validators=[validate_hash])
    
    def clean(self):
        cleaned_data=super().clean()
        firstpassword=cleaned_data.get("password")
        secondpassword=cleaned_data.get("repassword")
        
        if firstpassword and secondpassword:
            if isPasswordMatch(firstpassword,secondpassword)==False:
                raise forms.ValidationError("Password mismatch")
    
