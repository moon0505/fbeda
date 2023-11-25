      
from django.db import models
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
import time
from django.utils.text import slugify



class CaseManager(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150,null=False,unique=False,blank=False,
        verbose_name=("Unique Identification"))
    status=models.BooleanField(default=False)
    @property
    
    
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
class DataEntry(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    assignedCaseManagerSlug = models.CharField(max_length=20,blank=True,null=True)
    assignedStudentSlug = models.CharField(max_length=20,blank=True,null=True)

    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
    
      
    
class Student(models.Model):
        studentname= models.CharField(max_length=30,verbose_name= 'Name', null=True, blank=True)
        slug = models.SlugField(max_length=150,null=False,unique=False,blank=False,
        verbose_name=("Unique Identifier"),
        help_text=(
            "*Unique Identifier allows another to use FBO form if provided by you only"
        ),
    )
        # casemanager =  models.ForeignKey(CaseManager,on_delete=models.CASCADE, default=None)


        user_student = models.ForeignKey(User, on_delete=models.CASCADE,  default=None,related_name="postts")     

        def __str__(self):
          return str(self.studentname)


class Anticedent(models.Model):
        anticedentincident = models.CharField(max_length=50,verbose_name= 'Anticedent', null=True, blank=True)
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        
        anticedent_definition = models.CharField(null=True, blank=True, max_length=1000)
  
      
        user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        
        def __str__(self):
          return self.anticedentincident      
     

class Behavior(models.Model):
        behaviorincident = models.CharField(max_length=30,verbose_name= 'Behavior')
        behavior_definition = models.CharField(null=True, blank=True, max_length=1000,verbose_name= 'Behavior Definition')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        def __str__(self):
          return self.behaviorincident

              
class Function(models.Model):
        behaviorfunction = models.CharField(max_length=30, null=True, blank=True,verbose_name= 'Function')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
      
        user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        def __str__(self):
          return self.behaviorfunction  
      
      

class Consequence(models.Model):
        behaviorconsequence = models.CharField(max_length=30, null=True, blank=True,verbose_name= 'Consequence')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
      
        user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        def __str__(self):
          return self.behaviorconsequence  



class Enviroment(models.Model):
        behaviorenviroment = models.CharField(max_length=50, null=True, blank=True,verbose_name= 'Setting')
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        def __str__(self):
          return self.behaviorenviroment  
        

        

class Case(models.Model):
        student= models.ForeignKey(Student,on_delete=models.CASCADE)
        behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
        anticedent = models.ForeignKey(Anticedent,on_delete=models.CASCADE, verbose_name='Antecedent')
        function = models.ForeignKey(Function,on_delete=models.CASCADE)
        consequence = models.ForeignKey(Consequence,on_delete=models.CASCADE)
        enviroment = models.ForeignKey(Enviroment,on_delete=models.CASCADE, null=True, blank=True, verbose_name='Setting')

        date_created = models.DateField(null=True, blank=True, default=timezone.now)
        duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Duration')
        time = models.TimeField(null=True, blank=True)
        frequency = models.PositiveIntegerField(null=True, blank=True,  default=1, verbose_name='Frequency')

       
       
       
        class Meta:
            ordering = ['-date_created']
       
        def __str__(self):
          return str(self.student)

        def time_change(self):    
          return (time.strftime("%M:%S", time.gmtime(self.duration)) )  
      
      
      
      
      
      
# from django.views import generic
# from django.contrib.auth.models import User



# class CaseManager(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     slug = models.SlugField(max_length=150,null=False,unique=False,blank=False,
#         verbose_name=("slug"))
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
    
# class DataEntry(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     assignedCaseManagerSlug = models.CharField(max_length=20,blank=True,null=True)
#     assignedStudentSlug = models.CharField(max_length=20,blank=True,null=True)

#     admitDate=models.DateField(auto_now=True)
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
    
    
      
    
# class Student(models.Model):
#         studentname= models.CharField(max_length=30,verbose_name= 'Student Name', null=True, blank=True)
#         slug = models.SlugField(max_length=150,null=False,unique=False,blank=False,
#         verbose_name=("category safe URL"),
#         help_text=(
#             "format: required, letters, numbers, underscore, or hyphens"
#         ),
#     )

#         user_student = models.ForeignKey(User, on_delete=models.CASCADE,  default=None,related_name="postts")     

#         def __str__(self):
#           return str(self.studentname)


# class Anticendent(models.Model):
#         anticedentincident = models.CharField(max_length=30,verbose_name= 'Anticedent', null=True, blank=True)
#         student= models.ForeignKey(Student,on_delete=models.CASCADE)
        
#         anticedent_definition = models.CharField(null=True, blank=True, max_length=1000)
  
      
#         user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

        
#         def __str__(self):
#           return self.anticedentincident      
     

# class Behavior(models.Model):
#         behaviorincident = models.CharField(max_length=30)
#         behavior_definition = models.CharField(null=True, blank=True, max_length=1000)
#         student= models.ForeignKey(Student,on_delete=models.CASCADE)
#         user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

#         def __str__(self):
#           return self.behaviorincident

              
# class Function(models.Model):
#         behaviorfunction = models.CharField(max_length=30, null=True, blank=True)
#         student= models.ForeignKey(Student,on_delete=models.CASCADE)
      
#         user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)

#         def __str__(self):
#           return self.behaviorfunction  


# class Case(models.Model):
#         student= models.ForeignKey(Student,on_delete=models.CASCADE)
#         behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
#         user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
        