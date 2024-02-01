from django import forms
from django.contrib.auth.models import User
from bip import models
from django.forms import ModelForm
from .models import  Case, Behavior, Function, Student,Anticedent,Consequence, Enviroment,CustomUser
from django import forms
# from accounts.models import MyUser
from django.core.exceptions import ValidationError



# Old one down here try it

#for student related form
# class CaseManagerUserForm(forms.ModelForm):
    
#     class Meta:
#         model=CustomUser
#         fields=['first_name','last_name','username','password','bio','email',]
        # widgets = {
        # 'password': forms.PasswordInput()
        # }


# class CaseManagerUserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(), label="Password")
#     password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'username', 'email', 'bio']  # Removed 'password' from here, it's manually added above

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirmation = cleaned_data.get("password_confirmation")

#         if password and password_confirmation and password != password_confirmation:
#             msg = "The two password fields didn't match."
#             self.add_error('password_confirmation', msg)
#             # Or raise ValidationError(msg) if you want it to be form-wide rather than field-specific
            
#         return cleaned_data



class CaseManagerUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Makes the email field explicitly required

    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required.")
        # Add any additional custom validation for the email field here
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "The two password fields didn't match.")

        return cleaned_data
    

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
        model=CustomUser
        fields=['first_name','last_name','username','password','bio','email']
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
        fields = ('behavior','anticedent','consequence','function','date_created','time','duration','frequency','intensity','enviroment')
        widgets = {
            'date_created': DateInput(),
            'behavior':forms.RadioSelect(),
            'anticedent':forms.RadioSelect(),
            'function':forms.RadioSelect(),
            'consequence':forms.RadioSelect(),
            'enviroment': forms.Select(),  
            'time': forms.TimeInput(attrs={'placeholder': '12:00', 'type': 'time'}),

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
        fields = ('behaviorincident','behavior_definition','intensity_definition') 
        widgets = {
            'intensity_definition': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

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




class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')