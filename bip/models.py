   
from django.db import models
from django.views import generic
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
import time
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator




class CustomUser(AbstractUser):
    bio = models.CharField(max_length=45, blank=True, null=True, verbose_name='Occupation')

class CaseManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    slug = models.SlugField(max_length=150,null=True,unique=True,blank=True,
        verbose_name=("Unique Identification"))
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.status)
    
class DataEntry(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    assignedCaseManagerSlug = models.CharField(max_length=45,blank=True,null=True)
    assignedStudentSlug = models.CharField(max_length=45,blank=True,null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.status)



class Student(models.Model):
        GRADE_CHOICES = [
        ('TK', 'Transitional-Kindergarten'),
        ('K', 'Kindergarten'),
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        ('3', '3rd Grade'),
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
        ('8', '8th Grade'),
        ('9', '9th Grade'),
        ('10', '10th Grade'),
        ('11', '11th Grade'),
        ('12', '12th Grade'),
        ('AT', 'Adult Transition'),
        ('NA', 'Not Applicable'),


]
        studentname= models.CharField(max_length=30,verbose_name= 'Name')
        slug = models.SlugField(max_length=150,null=False,unique=False,blank=False,
        verbose_name=("Unique Identifier"),
        help_text=(
            "*Unique Identification allows another to use FBO form if provided by you only"
        ),
    )
        user_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None,related_name="postts")     
        age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Age')

        nonverbal=models.BooleanField(default=False,verbose_name='Nonverbal')
        grade = models.CharField(max_length=2, choices=GRADE_CHOICES, verbose_name='Grade', null=True, blank=True)

        def __str__(self):
          return str(self.studentname)

class Anticedent(models.Model):
        anticedentincident = models.CharField(max_length=50,verbose_name= 'Antecedent')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        anticedent_definition = models.CharField(null=True, blank=True, max_length=1000, verbose_name= 'Antecedent Definition')
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)
        def __str__(self):
          return self.anticedentincident      
     
class Behavior(models.Model):
        behaviorincident = models.CharField(max_length=30,verbose_name= 'Behavior')
        behavior_definition = models.CharField(null=True, blank=True, max_length=1000,verbose_name= 'Behavior Definition')
        intensity_definition = models.TextField(max_length=1000, null=True, blank=True,verbose_name= 'Define Intensity for 1(Mild), 2(Moderate), 3(Severe)')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)
        
        def __str__(self):
          return self.behaviorincident
          
class Function(models.Model):
        behaviorfunction = models.CharField(max_length=30, verbose_name= 'Function')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)
        def __str__(self):
          return self.behaviorfunction  
      
    
class Consequence(models.Model):
        behaviorconsequence = models.CharField(max_length=30, verbose_name= 'Consequence')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)
        def __str__(self):
          return self.behaviorconsequence  

class Enviroment(models.Model):
        behaviorenviroment = models.CharField(max_length=50, null=True, blank=True,verbose_name= 'Setting')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)

        
        
        # May need to check this if it causes issues with data table or more
        def __str__(self):
            return self.behaviorenviroment or ''
        
class Case(models.Model):
        
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
        anticedent = models.ForeignKey(Anticedent,on_delete=models.CASCADE, verbose_name='Antecedent')
        function = models.ForeignKey(Function,on_delete=models.CASCADE)
        consequence = models.ForeignKey(Consequence,on_delete=models.CASCADE)
        enviroment = models.ForeignKey(Enviroment,on_delete=models.CASCADE, null=True, blank=True, verbose_name='Setting')
        date_created = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='Date')
        duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Duration(Sec)')
        time = models.TimeField(null=True, blank=True)
        frequency = models.PositiveIntegerField(null=True, blank=True,  default=1, verbose_name='Frequency')
        intensity = models.PositiveIntegerField(null=True, blank=True,  default=1, validators=[
            MinValueValidator(1, message='Intensity must be at least 1(Mild).'),
            MaxValueValidator(3, message='Intensity options are 1(Mild), 2(Moderate),and 3(Severe).')
        ],
        verbose_name='Intensity')
      
    

        class Meta:
            ordering = ['-date_created']
       
        
        

        def __str__(self):
            return str(self.user) + ' - ' + str(self.student)


        def time_change(self):    
          return (time.strftime("%M:%S", time.gmtime(self.duration)) )  
      
      
      