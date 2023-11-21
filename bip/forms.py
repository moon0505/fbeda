from django import forms
from django.contrib.auth.models import User
from bip import models
from django.forms import ModelForm
from .models import  Case, Behavior, Function, Student,Anticedent,Consequence, Enviroment
from django import forms
# from accounts.models import MyUser


# Old one down here try it

#for student related form
class CaseManagerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
class CaseManagerForm(forms.ModelForm):
    class Meta:
        model=models.CaseManager
        fields=['slug','status']

class UpdateCaseManagerForm(forms.ModelForm):
    class Meta:
        model=models.CaseManager
        fields=['slug',]

#for teacher related form
class DataEntryUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
class DataEntryForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    # assignedCaseManagerSlug=forms.ModelChoiceField(queryset=models.CaseManager.objects.all().filter(status=True),empty_label="Token", to_field_name="user_id")
    
    assignedCaseManagerSlug=forms.CharField(max_length=20,required=False)
    assignedStudentSlug=forms.CharField(max_length=20,required=False)

    class Meta:
        model=models.DataEntry
        fields=['status']


# Behaviorforms-----------------------------------------------------------------------------

class DateInput(forms.DateInput):
    input_type = 'date'

class BehaviorForm(forms.ModelForm):
 
    class Meta():
        model = Case
        fields = ('behavior','anticedent','consequence','function','date_created','time','duration','frequency','enviroment')
        widgets = {
            'date_created': DateInput(),
            'behavior':forms.RadioSelect(),
            'anticedent':forms.RadioSelect(),
            'function':forms.RadioSelect(),
            'consequence':forms.RadioSelect(),
            # 'enviroment':forms.RadioSelect(),
            'enviroment': forms.Select(attrs={'class': 'form-control'}),  


            

        }


   


   
class StudentForm(ModelForm):
    class Meta():
        model = Student
        fields = ('studentname',) 
        
        
class StudentUpdateForm(ModelForm):
    class Meta():
        model = Student
        fields = ('studentname','slug') 
 
class StudentFormSlug(ModelForm):
    class Meta():
        model = Student
        fields = ('slug',) 
        
        
   
class CreateBehaviorForm(ModelForm):
    class Meta():
        model = Behavior
        fields = ('behaviorincident','behavior_definition') 

class CreateAnticedentForm(ModelForm):
    class Meta():
        model = Anticedent
        fields = ('anticedentincident','anticedent_definition') 
 
class CreateFunctionForm(ModelForm):
    class Meta():
        model = Function
        fields = ('behaviorfunction',) 
 
 
 
class CreateConsequenceForm(ModelForm):
    class Meta():
        model = Consequence
        fields = ('behaviorconsequence',) 



class CreateEnviromentForm(ModelForm):
    class Meta():
        model = Enviroment
        fields = ('behaviorenviroment',)

class StudentBehaviorForm(ModelForm):
    class Meta():
        model = Behavior
        fields = '__all__'    
        
FORMAT_CHOICES ={
    ('xlsx', 'xlsx'),
    ('csv', 'csv'),
    ('json', 'json'),
}

class FormatForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))