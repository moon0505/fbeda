from django.shortcuts import render, redirect, get_object_or_404 
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.urls import reverse
from bip import models
from django.urls import reverse_lazy

from django.contrib.auth.models import User 
from . import forms
from django.contrib.auth.models import Group

from bip.forms import CaseManagerUserForm, CaseManagerForm
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.contrib.auth.decorators import login_required,user_passes_test

from .models import   Student, Behavior, Case, Anticedent, Function, Consequence,Enviroment
from .forms import BehaviorForm, StudentForm,StudentUpdateForm, CreateBehaviorForm,CreateAnticedentForm,CreateFunctionForm, CreateConsequenceForm, StudentFormSlug, UpdateCaseManagerForm,CreateEnviromentForm
from .utils import  (
    get_bar_chart,
    get_clustermap,
    get_multiple_line_plot_one,
    
    get_multiple_line_plot_two,
    get_multiple_line_plot_three,
    get_multiple_line_plot_four,
    get_multiple_line_plot_five,
    get_multiple_line_plot_chatgpt,
    get_heatmap,
    get_box_plot,
    get_count_beh_plot,
    get_multiple_scatter_plot_one,
    get_multiple_scatter_plot_two,
    get_multiple_scatter_plot_three,
    get_multiple_scatter_plot_four,
    get_multiple_scatter_plot_five,
    get_pie_chart,
    get_pie__chart_anticedent,
    get_pie__chart_function,
    get_duration_bar_chart,
    get_pie__chart_consequence,
    get_box_plot_function,
    get_box_plot_consequence,
    get_box_plot_setting,
    
    
    )
import pandas as pd
import numpy as np
import csv

import requests
from docx import Document
from django.shortcuts import render
from urllib.parse import unquote
import html2text


def home(request):
  
  
    return render(request,'bip/home.html')




def luna(request):
    
    return render(request,'bip/home.html')


def error_page(request,  pk):
  
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all()
  

    context ={"student_cases":student_cases,'student':student}

    return render(request,'bip/error_page.html',context)

def description_view(request):
  
  
    return render(request,'bip/description.html')
  
# Below login and logout views are for case manager and data entry

#for showing signup/login button for doctor(by sumit)
def casemangerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'account/casemanagerclick.html')


#for showing signup/login button for patient(by sumit)
def dataentryclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'account/dataentryclick.html')



def case_manager_signup_view(request):
    userForm=forms.CaseManagerUserForm()
    caseManagerForm=forms.CaseManagerForm()
    mydict={'userForm':userForm,'caseManagerForm':caseManagerForm}
    if request.method=='POST':
        userForm=forms.CaseManagerUserForm(request.POST)
        caseManagerForm=forms.CaseManagerForm(request.POST,request.FILES)
        if userForm.is_valid() and caseManagerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            casemanager=caseManagerForm.save(commit=False)
            casemanager.user=user
            casemanager=casemanager.save()
            casemanager_group = Group.objects.get_or_create(name='CASE MANAGER')
            casemanager_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('bip:case_manager_login'))
    return render(request,'account/case_manager_signup.html',context=mydict)

        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




def data_entry_signup_view(request):
    userForm=forms.DataEntryUserForm()
    dataEntryForm=forms.DataEntryForm()
    mydict={'userForm':userForm,'dataEntryForm':dataEntryForm}
    if request.method=='POST':
        userForm=forms.DataEntryUserForm(request.POST)
        dataEntryForm=forms.DataEntryForm(request.POST,request.FILES)
        if userForm.is_valid() and dataEntryForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            dataentry =dataEntryForm.save(commit=False)
            dataentry.user=user
            
            dataentry.assignedCaseManagerSlug=request.POST.get('assignedCaseManagerSlug')
            dataentry.assignedStudentSlug=request.POST.get('assignedStudentSlug')
            dataentry=dataentry.save()
            my_dataentry_group = Group.objects.get_or_create(name='DATA ENTRY')
            my_dataentry_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('bip:data_entry_login'))
    return render(request,'account/data_entry_signup.html',context=mydict)

        # return HttpResponseRedirect(reverse('bip:case_manager_login'))


def is_case_manager(user):
    return user.groups.filter(name='CASE MANAGER').exists()
def is_data_entry(user):
    return user.groups.filter(name='DATA ENTRY').exists()

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('bip:description'))




#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF Casemanager,Dataentry or not



def afterlogin_view(request):
    if  is_case_manager(request.user):
        accountapproval=models.CaseManager.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('home/')
        else:
            return render(request,'account/case_manager_wait_for_approval.html')
    elif is_data_entry(request.user):
        accountapproval=models.DataEntry.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('bip:data_entry_dashboard')
        else:
            return render(request,'account/data_entry_wait_for_approval.html')


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF Casemanager,Dataentry or not


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def case_manager_dashboard_view(request):
    
    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)

    try:
        specific_data_entry =models.DataEntry.objects.get(assignedCaseManagerSlug=case_manager_entry.slug)
        print(specific_data_entry)
    except:
        specific_data_entry =None

    mydict={
        'specific_data_entry':specific_data_entry,
   
    }
    return render(request,'account/case_manager_dashboard.html',context=mydict)


@login_required(login_url='data_entry_login')
@user_passes_test(is_data_entry)
def data_entry_dashboard_view(request):
    
    data_entry =models.DataEntry.objects.get(user_id=request.user.id)
    case_manager=models.CaseManager.objects.get(slug=data_entry.assignedCaseManagerSlug)
    
    
    assigned_student =models.Student.objects.get(slug=data_entry.assignedStudentSlug)
 
    mydict={
    'data_entry':data_entry,
    'case_manager':case_manager,
    'case_manager_name':case_manager.get_name,
    'assigned_student':assigned_student,
    
    }
    return render(request,'account/data_entry_dashboard.html',context=mydict)


def data_entry_input_view(request, pk):
  
    student = get_object_or_404(Student, pk=pk)
    
    student_behaviors = student.case_set.all()[:10] 
    

    # products = Product.objects.all()[:10]


    behavior = Behavior.objects.all()
   
      
    case = Case.objects.all()
          
    
    # this works:
    stbehavior = student.behavior_set.all() 
      
        
    behaivorpest  = behavior.filter(pk=pk).filter(behaviorincident__icontains="behaviorincident")
    
    context = {'student_behaviors':student_behaviors,
               "student":student,
           
               }
     
    return render(request, 'bip/data_entry_input.html',context, )



@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def admin_approve_data_entry_view(request):
    #those whose approval are needed
  
    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)
    
    specific_data_entry =models.DataEntry.objects.get(assignedCaseManagerSlug=case_manager_entry.slug)
    
   

    context = {
        'specific_data_entry':specific_data_entry
        }
    
    return render(request,'account/admin_data_entry_approve.html',context)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def approved_data_entry_view(request,pk):
    data_entry=models.DataEntry.objects.get(id=pk)
    data_entry.status=True
    data_entry.save()
    return redirect(reverse('bip:case_manager_dashboard'))


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def admin_delete_data_entry_view(request):
    
    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)
    
    specific_data_entry =models.DataEntry.objects.get(assignedCaseManagerSlug=case_manager_entry.slug)
    
    
    context = { 
               'specific_data_entry':specific_data_entry,
               }
    
    return render(request,'account/admin_delete_data_entry.html',context)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def delete_data_entry_view(request,pk):
    data_entry=models.DataEntry.objects.get(id=pk)
    user=models.User.objects.get(id=data_entry.user_id)
    user.delete()
    data_entry.delete()
    return redirect('bip:case_manager_dashboard')


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def reject_data_entry_view(request,pk):
    data_entry=models.DataEntry.objects.get(id=pk)
    user=models.User.objects.get(id=data_entry.user_id)
    user.delete()
    data_entry.delete()
    return redirect('bip:case_manager_dashboard')


# Website forms/input---------------------------------------------------------


class UserPosts(LoginRequiredMixin, generic.ListView):
    model = models.Student
    template_name = "bip/student_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("postts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.postts.all()



class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'bip/welcome_user.html'


@login_required
def list_view(request,pk):
    student = get_object_or_404(Student, pk=pk)
    student_list = student.case_set.all()

    context ={"student_list":student_list,'student':student}
         
    return render(request, "bip/student_list.html", context)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def dashboard(request, pk):
  
    student = get_object_or_404(Student, pk=pk)

    student_behaviors = student.case_set.all() 

    student_duration = Case.objects.filter(student__id=pk).values('duration')



    # delete
    firstduration = student_duration.first()

    # print(firstduration)



    behavior = Behavior.objects.all()

          
    context = {
    'student_behaviors':student_behaviors,
    "student":student,
    'student_duration':student_duration,
    'firstduration':firstduration,
    
               }
    
    return render(request, 'bip/dashboard.html',context, )


@login_required
def behavior_form_view(request, pk):

    student = Student.objects.get(id=pk) 
    behaviorset = student.behavior_set.all()
    anticedentset = student.anticedent_set.all()
    functionset = student.function_set.all()
    consequset = student.consequence_set.all()
    enviromentset = student.enviroment_set.all()

    

    if request.method == 'POST':
        form = BehaviorForm(instance=student) 
        form = BehaviorForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.student = student
            instance.save()   


            if is_case_manager(request.user):
                return redirect("bip:dashboard", student.id)

            elif is_data_entry(request.user):
                return redirect("bip:data_entry_input", student.id)
            
            

                

    else:
        form = BehaviorForm()                                            
        form.fields["behavior"].queryset=behaviorset
        form.fields["anticedent"].queryset=anticedentset
        form.fields["consequence"].queryset=consequset
        form.fields["function"].queryset=functionset
        form.fields["enviroment"].queryset=enviromentset

        
    return render(request, 'bip/fbo_form.html', {'form': form,'student':student})



@login_required      
def updatePost(request, pk,student_id ):
    
    student_post = Case.objects.get(id=pk, student_id= student_id) 
    form = BehaviorForm(instance=student_post)
    behaviors = Behavior.objects.all()
    behaivorpest  = Behavior.objects.filter(user=request.user,student_id=student_id)
    anticedentpest  = Anticedent.objects.filter(user=request.user,student_id=student_id)
    functionpest  = Function.objects.filter(user=request.user,student_id=student_id)
        
    if request.method == 'POST': 
      form = BehaviorForm(request.POST, instance=student_post) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:dashboard", student_post.student.id)
    
    else:
        form = BehaviorForm(instance=student_post)                                           
        form.fields["behavior"].queryset=behaivorpest
        form.fields["anticedent"].queryset=anticedentpest
        form.fields["function"].queryset=functionpest
    
    context = {'form':form,
            'student_post':student_post,
               }
    
    return render(request, "bip/update_post.html", context)


def deletePost(request, pk):
  behavior_incident = Case.objects.get(id=pk)
  
  if request.method == 'POST': 
    behavior_incident.delete()
    return redirect("bip:dashboard", behavior_incident.student.id)
  
  
  context = {'incident': behavior_incident}
  return render(request, 'bip/delete_post.html', context)


@login_required
def create_student(request):
    user_student = User.objects.get(pk=request.user.id)
    form = StudentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = StudentForm(request.POST)   
            
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user_student = User.objects.get(pk=request.user.id)
                 obj.save()                 
                
                 return redirect("bip:for_user", username=request.user.username)
                
            else:
                print("ERROR In Form") 
     
    return render(request, 'bip/create_student.html', {'form': form,'user_student':user_student})


def updateStudent(request, pk):
        
    studentupdate = Student.objects.get(id=pk)

    form = StudentUpdateForm(instance=studentupdate)
    
    if request.method == 'POST': 
      form = StudentUpdateForm(request.POST, instance=studentupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:dashboard", studentupdate.id)
    
   
    context = {'form':form}
    
    return render(request, "bip/create_student.html", context)


def deleteStudent(request, pk):
    
    studentdelete = Student.objects.get(id=pk)
    
    student = Student.objects.get(id=pk)
    
    if request.method == "POST":
        studentdelete.delete()
        return redirect("bip:home")
    
    context = {'item':studentdelete,'student':student}
    return render(request, "bip/delete_student.html", context)

@login_required
def create_behavior(request,pk):
    user = User.objects.get(pk=request.user.id)
    student = Student.objects.get(id=pk) 

    form = CreateBehaviorForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateBehaviorForm(request.POST)
            
            
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = User.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save()
                 return redirect("bip:dashboard", student.id)                
                
                             
            else:
                print("ERROR In Form") 
            
    
     
    return render(request, 'bip/create_behavior.html', {'form': form})
# #  



def updateBehavior(request, pk):
    
    behupdate = Behavior.objects.get(id=pk)

      
    form = CreateBehaviorForm(instance=behupdate)
    
    if request.method == 'POST': 
      form = CreateBehaviorForm(request.POST, instance=behupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:edit_behavior", behupdate.student.id)
    
   
    context = {'form':form}
    
    return render(request, "bip/update_behavior.html", context)




def deleteBehavior(request, pk):
    
    behdelete = Behavior.objects.get(id=pk)
    print(behdelete)
    
    if request.method == "POST":
        behdelete.delete()
        return redirect("bip:abc", behdelete.student.id)
    
    context = {'item':behdelete}
    return render(request, "bip/delete_behavior.html", context)




# Use pk to createbehavior
@login_required
def create_anticedent(request,pk):
    user = User.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateAnticedentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateAnticedentForm(request.POST)

            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = User.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save() 
                 return redirect("bip:dashboard", student.id)                 
     
            else:
                print("ERROR In Form") 
    return render(request, 'bip/create_anticedent.html', {'form': form})
      

def updateAnticedent(request, pk):
        
    antiupdate = Anticedent.objects.get(id=pk)
    form = CreateAnticedentForm(instance=antiupdate)
    
    if request.method == 'POST': 
      form = CreateAnticedentForm(request.POST, instance=antiupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user   
          instance.save()       
          return redirect("bip:abc", antiupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_anticedent.html", context)

def deleteAnticedent(request, pk):
    
    antidelete = Anticedent.objects.get(id=pk)
    
    if request.method == "POST":
        antidelete.delete()
        return redirect("bip:abc", antidelete.student.id)
    
    context = {'item':antidelete}
    return render(request, "bip/delete_anticedent.html", context)

@login_required
def create_function(request,pk):
    user = User.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateFunctionForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateFunctionForm(request.POST)
        
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = User.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save()
                 return redirect("bip:dashboard", student.id)                              
                
            else:
                print("ERROR In Form") 

    return render(request, 'bip/create_function.html', {'form': form})



def updatFunction(request, pk):
        
    funcupdate = Function.objects.get(id=pk)

    form = CreateFunctionForm(instance=funcupdate)
    
    if request.method == 'POST': 
      form = CreateFunctionForm(request.POST, instance=funcupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user  
          instance.save()  
          
          return redirect("bip:abc", funcupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_function.html", context)


def deleteFunction(request, pk):
    
    funcdelete = Function.objects.get(id=pk)
    
    if request.method == "POST":
        funcdelete.delete()
        return redirect("bip:abc", funcdelete.student.id)
    
    context = {'item':funcdelete}
    return render(request, "bip/delete_function.html", context)


@login_required
def create_consequence(request,pk):
    user = User.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateConsequenceForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateConsequenceForm(request.POST)

            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = User.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save() 
                 return redirect("bip:dashboard", student.id)                 
     
            else:
                print("ERROR In Form") 
    return render(request, 'bip/create_consequence.html', {'form': form})



def updateConsequence(request, pk):
        
    conqupdate = Consequence.objects.get(id=pk)

    form = CreateConsequenceForm(instance=conqupdate)
    
    if request.method == 'POST': 
      form = CreateConsequenceForm(request.POST, instance=conqupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user  
          instance.save()  
          
          return redirect("bip:abc", conqupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_consequence.html", context)


def deleteConsequence(request, pk):
    
    conqdelete = Consequence.objects.get(id=pk)
    
    if request.method == "POST":
        conqdelete.delete()
        return redirect("bip:abc", conqdelete.student.id)
    
    context = {'item':conqdelete}
    return render(request, "bip/delete_consequence.html", context)

@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def abc_view(request, pk ):
    student = Student.objects.get(id=pk) 
    
    function = Function.objects.all()
    functionset = student.function_set.all()

    anticedent = Anticedent.objects.all()
    anticedentset = student.anticedent_set.all()
    
    behaviors = Behavior.objects.all()
    behaivorpest  = Behavior.objects.filter(user=request.user)
    behaviorset = student.behavior_set.all()
    
     
    consequence = Consequence.objects.all()
    consequencepest  = Consequence.objects.filter(user=request.user)
    conseqenceset = student.consequence_set.all()
    
    
     
    context= {
        'behaviorset':behaviorset,
        'anticedentset':anticedentset,
        'functionset': functionset,
        'conseqenceset':conseqenceset,
        'student':student,  
    }
    
    return render(request, 'bip/abc.html', context)

@login_required
def create_setting_view(request,pk):
    user = User.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateEnviromentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateEnviromentForm(request.POST)
        
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = User.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save()
                 return redirect("bip:dashboard", student.id)                              
                
            else:
                print("ERROR In Form") 

    return render(request, 'bip/create_setting.html', {'form': form})


def updateSetting(request, pk):
        
    enviromentupdate = Enviroment.objects.get(id=pk)

    form = CreateEnviromentForm(instance=enviromentupdate)
    
    if request.method == 'POST': 
      form = CreateEnviromentForm(request.POST, instance=enviromentupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user  
          instance.save()  
          
          return redirect("bip:update_setting", enviromentupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_setting.html", context)

def deleteEnviroment(request, pk):
    
    envdelete = Enviroment.objects.get(id=pk)
    
    if request.method == "POST":
        envdelete.delete()
        return redirect("bip:edit_setting", envdelete.student.id)
    
    context = {'item':envdelete}
    return render(request, "bip/delete_setting.html", context)

@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def edit_enviroment_view(request, pk ):
    student = Student.objects.get(id=pk) 
   
    enviroment = Enviroment.objects.all()
    enviromentset = student.enviroment_set.all()


  
    context= {
        'enviromentset':enviromentset,   
        'student':student,  
    }
    
    return render(request, 'bip/edit_setting.html', context)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def edit_behavior_view(request, pk ):
    student = Student.objects.get(id=pk) 
    
    behaviors = Behavior.objects.all()
    behaivorpest  = Behavior.objects.filter(user=request.user)
    behaviorset = student.behavior_set.all()
    
     
     
    context= {
        'behaviorset':behaviorset,
       
        'student':student,  
    }
    
    return render(request, 'bip/edit_behavior.html', context)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)

def edit_anticedent_view(request, pk ):
    student = Student.objects.get(id=pk) 
   
    anticedent = Anticedent.objects.all()
    anticedentset = student.anticedent_set.all()
  
    context= {
        'anticedentset':anticedentset,   
        'student':student,  
    }
    
    return render(request, 'bip/edit_anticedent.html', context)



@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def edit_consequence_view(request, pk ):
    student = Student.objects.get(id=pk) 
    
    
    
     
    consequence = Consequence.objects.all()
    consequencepest  = Consequence.objects.filter(user=request.user)
    conseqenceset = student.consequence_set.all()
    
    
     
    context= {
       
        'conseqenceset':conseqenceset,
        'student':student,  
    }
    
    return render(request, 'bip/edit_consequence.html', context)

@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def edit_function_view(request, pk ):
    student = Student.objects.get(id=pk) 
    
    function = Function.objects.all()
    functionset = student.function_set.all()

    context= {
       
        'functionset': functionset,
       
        'student':student,  
    }
    
    return render(request, 'bip/edit_function.html', context)



@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def student_profile(request, pk ):
    student = Student.objects.get(id=pk) 
    
         
    context= {
       
        'student':student,  
    }
    return render(request, 'bip/student_profile.html', context)
# Exploratory 
# 
# 
# 
# Data Analysisxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def snapshot_view(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    

    cases_df = pd.DataFrame(data)

    # print(cases_df)
      
    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        # cases_df.columns = cases_df.columns.astype(str).str.replace('behavior__behaviorincident', 'Behavior')

        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)



    
  
    df1 = cases_df['Date'].value_counts()

    # print(df1)

    df1 = df1.to_frame().reset_index() 

    # print(df1)

    df2 = df1.reset_index()

    # print(df2)


    df2 = df2.sort_values(by=['index'])

    # print(df2)


    df3 = df2['Date']

    # print(df3)
    
    df4 = df2['count']

    # print(df4)

    bar_graph = get_bar_chart(x=df3, y = df4)
  
    
    # multiple dddbar graph- line plot origniallyxxxxxxxxxxxxxxxxxxxxxxxxx
  
    
    df_multiple_bar = cases_df[['Behavior','Date']]

    pivot = pd.pivot_table(df_multiple_bar,  
                                index='Date', 
                                columns='Behavior', 
                                aggfunc=len,fill_value=0)
    
    
    dlpivot = pivot.reset_index()
    
    
    multiple_line_plot_five = None
    
    
    try:       
    
        multiple_line_plot_five = get_multiple_line_plot_five(
            x=dlpivot['Date'],y=dlpivot.iloc[:,1],data=dlpivot,
            z=dlpivot['Date'], k=dlpivot.iloc[:,2],data1=dlpivot,
            g=dlpivot['Date'], q=dlpivot.iloc[:,3],data2=dlpivot,
            m=dlpivot['Date'], n=dlpivot.iloc[:,4],data3=dlpivot,
            b=dlpivot['Date'], c=dlpivot.iloc[:,5],data4=dlpivot
        )
     
    except:
        pass
    
    
    multiple_line_plot_four = None
 
    try:       
    
        multiple_line_plot_four = get_multiple_line_plot_four(
            x=dlpivot['Date'],y=dlpivot.iloc[:,1],data=dlpivot,
            z=dlpivot['Date'], k=dlpivot.iloc[:,2],data1=dlpivot,
            g=dlpivot['Date'], q=dlpivot.iloc[:,3],data2=dlpivot,
            m=dlpivot['Date'], n=dlpivot.iloc[:,4],data3=dlpivot
        )
     
    except:
        pass
    
    
    multiple_line_plot_three = None

    try:       
    
        multiple_line_plot_three = get_multiple_line_plot_three(
            x=dlpivot['Date'],y=dlpivot.iloc[:,1],data=dlpivot,
            z=dlpivot['Date'], k=dlpivot.iloc[:,2],data1=dlpivot,
            g=dlpivot['Date'], q=dlpivot.iloc[:,3],data2=dlpivot,
        )
     
    except:
        pass
    
    
    multiple_line_plot_two = None
    
    try:       
    
        multiple_line_plot_two = get_multiple_line_plot_two(
            x=dlpivot['Date'],y=dlpivot.iloc[:,1],data=dlpivot,
            z=dlpivot['Date'], k=dlpivot.iloc[:,2],data1=dlpivot,
        )
     
    except:
        pass
    
    
    multiple_line_plot_one = None

    try:       
    
        multiple_line_plot_one = get_multiple_line_plot_one(
            x=dlpivot['Date'],y=dlpivot.iloc[:,1],data=dlpivot
        )
     
    except:
        pass
    
    
    multiple_line_plot_chatgpt = None
    y_column_name = 'Behavior'  # Replace with the actual desired column name

# Check if the selected column has any data
    if y_column_name in dlpivot.columns and len(dlpivot[y_column_name]) > 0:
        multiple_line_plot_chatgpt = get_multiple_line_plot_chatgpt(
            x=dlpivot['Date'],
            y=dlpivot[y_column_name],
            data=dlpivot
    )
    else:
        print("Selected y column is empty or does not exist.")
  
  
    # cluster heatmapcorrelation matrixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])
    
    
    df_matrix = pd.concat([cases_df,behavior, anticedent,function], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 

    # print(matrix)
  

    iclustermap_graph = None
    
    try:
        iclustermap_graph = get_clustermap(data=matrix)

    except:
        pass
  


# heatmap correaltion matrix
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])
    
    
    df_matrix = pd.concat([cases_df,behavior, anticedent,function], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 

    # print(matrix)
  

    
    iheat_graph = None
    
    try:
        iheat_graph = get_heatmap(data=matrix)

    except:
        pass
  

  
  
    context= {
    
        'student':student,
        'bar_graph':bar_graph,
        'iheat_graph':iheat_graph,
        'iclustermap_graph':iclustermap_graph, 
        'multiple_line_plot_one':multiple_line_plot_one,
        'multiple_line_plot_two':multiple_line_plot_two,
        'multiple_line_plot_three':multiple_line_plot_three,
        'multiple_line_plot_four':multiple_line_plot_four,
        'multiple_line_plot_five':multiple_line_plot_five, 
        'multiple_line_plot_chatgpt':multiple_line_plot_chatgpt,
    }
    
    return render(request, 'bip/snapshot.html', context)





# xxxxxxxxxxx

def snapshot_data_entry_view(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    

    cases_df = pd.DataFrame(data)

    # print(cases_df)
      
    
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
  
  
    df1 = cases_df['Date'].value_counts()

    # print(df1)

    df1 = df1.to_frame().reset_index() 

    # print(df1)

    df2 = df1.reset_index()

    # print(df2)


    df2 = df2.sort_values(by=['index'])

    # print(df2)


    df3 = df2['Date']

    # print(df3)
    
    df4 = df2['count']

    print(df4)

    bar_graph = get_bar_chart(x=df3, y = df4)
  
    
  
    
    context= {
    
        'student':student,
        'bar_graph':bar_graph,
       
    }
    
    return render(request, 'bip/data_entry_chart_view.html', context)






# xxxxxxxx


def function_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    
    cases_df = pd.DataFrame(data)
      
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    
    
    df_function = cases_df['Function']
    
    
    box_graph_function = get_box_plot_function( x= df_function, data=cases_df) 
    
    
    # correationxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])
    
    
    df_matrix = pd.concat([cases_df,behavior,function], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 
  



    try:
        filterDX = matrix[((matrix > 0.0)) & (matrix != 1.000)]
    
        iheat_graph = get_heatmap(data=filterDX)
    except:
        pass
    

    iclustermap_graph = None
    
    try:
        iclustermap_graph = get_clustermap(data=matrix)

    except:
        pass
  
  

    context= {'student':student,'iclustermap_graph':iclustermap_graph, 
    'iheat_graph':iheat_graph, 
    'box_graph_function':box_graph_function,}
    
    
    return render(request, 'bip/function.html', context)



def consequence_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'consequence__behaviorconsequence','date_created','time','id')
    
    cases_df = pd.DataFrame(data)
      
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    
    
    df_consequence = cases_df['Consequence']
    
    
    box_graph_consequence = get_box_plot_consequence( x= df_consequence, data=cases_df) 
    
    
    # correationxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])
    
    consequence = pd.get_dummies(cases_df['Consequence'])

    
    df_matrix = pd.concat([cases_df,behavior,consequence], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Consequence', 'Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 
  
# stopped here


    try:
        filterDX = matrix[((matrix > 0.0)) & (matrix != 1.000)]
    
        iheat_graph = get_heatmap(data=filterDX)
    except:
        pass
    

    iclustermap_graph = None
    
    try:
        iclustermap_graph = get_clustermap(data=matrix)

    except:
        pass
  
  

    context= {'student':student,'iclustermap_graph':iclustermap_graph, 
    'iheat_graph':iheat_graph, 
    'box_graph_consequence':box_graph_consequence,}
    
    
    return render(request, 'bip/consequence.html', context)




def anticedent_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    
    cases_df = pd.DataFrame(data)
      
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    
    
    
    
    df_anticedent = cases_df['Anticedent']
    
    
    box_graph = get_box_plot( x= df_anticedent, data=cases_df) 
    
    
    # correationxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])
    
    
    df_matrix = pd.concat([cases_df,behavior,anticedent], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 
  

    try:
        filterDX = matrix[((matrix > 0.0)) & (matrix != 1.000)]
    
        iheat_graph = get_heatmap(data=filterDX)
    except:
        pass
    

    iclustermap_graph = None
    
    try:
        iclustermap_graph = get_clustermap(data=matrix)

    except:
        pass
  
  

    context= {'student':student,'iclustermap_graph':iclustermap_graph, 
    'iheat_graph':iheat_graph, 
    'box_graph':box_graph,}
    
    
    return render(request, 'bip/anticedent.html', context)

    

# Setting enviroment
def enviroment_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'enviroment__behaviorenviroment','date_created','time','id')
    
    cases_df = pd.DataFrame(data)
      
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('enviroment__behaviorenviroment', 'Enviroment')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    
    df_enviroment = cases_df['Enviroment']

    box_graph_setting = get_box_plot_setting( x= df_enviroment, data=cases_df) 



    # correationxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    
    function = pd.get_dummies(cases_df['Function'])

    enviroment = pd.get_dummies(cases_df['Enviroment'])

    df_matrix = pd.concat([cases_df,behavior,enviroment], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Enviroment','Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 
  

    try:
        filterDX = matrix[((matrix > 0.0)) & (matrix != 1.000)]
    
        iheat_graph = get_heatmap(data=filterDX)
    except:
        pass
    

    iclustermap_graph = None
    
    try:
        iclustermap_graph = get_clustermap(data=matrix)

    except:
        pass
  
  

    context= {'student':student,'iclustermap_graph':iclustermap_graph, 
    'iheat_graph':iheat_graph, 
    'box_graph_setting':box_graph_setting,}
    
    
    return render(request, 'bip/setting.html', context)


# end of enviroment setting

def is_valid_queryparam(param):
    return param != '' and param is not None

# def filter_data(request, pk):
   
#     student = get_object_or_404(Student, pk=pk)

#     student_cases = student.case_set.all() 
#     behaviorset = student.behavior_set.all()
#     functionset = student.function_set.all()
#     anticedentset = student.anticedent_set.all()
#     consequenceset = student.consequence_set.all()

#     case = Case.objects.all()

#     bqs =  student.behavior_set.all() 
    
    
#     fqs =  student.function_set.all()
#     aqs =  student.anticedent_set.all() 
#     dateqs = student.case_set.all()
    
    
#     total_beh = student.case_set.count()
    
    
#     behavior_query = request.GET.get('behavior')
#     function_query = request.GET.get('function')
#     anticedent_query = request.GET.get('anticedent')
#     consequence_query = request.GET.get('consequence')
#     date_min = request.GET.get('date_min')
#     date_max = request.GET.get('date_max')
    
#     qs = None
    
#     qs_count = None
    
    
#     if is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(function_query) and function_query != 'Choose Function' and  is_valid_queryparam(date_min) and is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) &  student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(function__behaviorfunction=function_query)  & student_cases.filter(date_created__gte=date_min) & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()
        
        
#         # works
        
        
        
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(function_query) and function_query != 'Choose Function' and is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(function__behaviorfunction=function_query)   & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()
        
  
#     # work 
    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(function_query) and function_query != 'Choose Function' and is_valid_queryparam(date_min):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(function__behaviorfunction=function_query)  & student_cases.filter(date_created__gte=date_min)
        
#         qs_count = qs.count()
        
      
    
#     # work
       
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(function_query) and function_query != 'Choose Function':
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) &  student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(function__behaviorfunction=function_query)
    
#         qs_count = qs.count()
        
        
#     # work
    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(date_min) and is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(date_created__gte=date_min) & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()
        
    
    
    
#     # work
    
    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and consequence_query != 'Choose Consequence' and is_valid_queryparam(date_min):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query) & student_cases.filter(date_created__gte=date_min) 
        
#         qs_count = qs.count()
 
 
# #  work
    
    
    
     
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and consequence_query != 'Choose Consequence' and  is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query)  & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()

    
    
#     # work
    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence':
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(consequence__behaviorconsequence=consequence_query)  
        
#         qs_count = qs.count()
    
#     # work
    
    
    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and function_query != 'Choose Function' and is_valid_queryparam(date_min) and is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(function__behaviorfunction=function_query) & student_cases.filter(date_created__gte=date_min) & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()
        
#      # work
    
    
  
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and function_query != 'Choose Function' and is_valid_queryparam(date_min):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(function__behaviorfunction=function_query) & student_cases.filter(date_created__gte=date_min) 
        
        
#         qs_count = qs.count()
        
        
        
#         # check min
        
        
     
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and function_query != 'Choose Function':
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(function__behaviorfunction=function_query) 
        
        
#         qs_count = qs.count()
       
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' :
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(anticedent__anticedentincident=anticedent_query) 
        
#         qs_count = qs.count()






    
    
#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and  is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence':
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(consequence__behaviorconsequence=consequence_query)  
        
#         qs_count = qs.count()


#     # works 










#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior' and is_valid_queryparam(function_query) and function_query != 'Choose Function' :
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(function__behaviorfunction=function_query) 
    
#         qs_count = qs.count()

    
#     elif  is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' and is_valid_queryparam(function_query) and function_query != 'Choose Function':
        
#         qs =  student_cases.filter(anticedent__anticedentincident=anticedent_query) & student_cases.filter(function__behaviorfunction=function_query) 
        
        
#         qs_count = qs.count()



#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior'  and is_valid_queryparam(date_min) and is_valid_queryparam(date_max):
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  & student_cases.filter(date_created__gte=date_min) & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()

#     elif is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior':
        
#         qs = student_cases.filter(behavior__behaviorincident = behavior_query)  
#         qs_count = qs.count()
  
  
  
  
  
#     elif is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent' :
        
#         qs = student_cases.filter(anticedent__anticedentincident=anticedent_query) 
        
#         qs_count = qs.count()
        
        
    
#     elif  is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence':
        
#         qs =  student_cases.filter(consequence__behaviorconsequence=consequence_query)  
        
#         qs_count = qs.count()

   
#     elif  is_valid_queryparam(function_query) and function_query != 'Choose Function' :
        
#         qs =student_cases.filter(function__behaviorfunction=function_query) 
    
#         qs_count = qs.count()

#     elif is_valid_queryparam(date_min) and is_valid_queryparam(date_max):
#         qs =  student_cases.filter(date_created__gte=date_min) & student_cases.filter(date_created__lt=date_max)
        
#         qs_count = qs.count()
        
#     elif is_valid_queryparam(date_min) :
#         qs =  student_cases.filter(date_created__gte=date_min) 
        
#         qs_count = qs.count()
        
#     elif  is_valid_queryparam(date_max):
#         qs =  student_cases.filter(date_created__lt=date_max)
        
        
#         qs_count = qs.count()

#     beh_devide = None
#     if qs_count:
#         beh_devide = qs_count / total_beh * 100
    
#     context = {'queryset': qs,
#                'student_cases':student_cases,
#                'behaviorset':behaviorset,
#                'anticedentset':anticedentset, 
#                "functionset":functionset,
#                "consequenceset":consequenceset,
#                'case':case,
#                'qs_count':qs_count,
#                'student':student,
#                'values':request.GET,
#                'total_beh':total_beh,
#                'beh_devide':beh_devide
#                            }
    
#     return render(request, 'bip/filter_data.html', context)


from django.db.models import Q

def filter_data(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all()

    behavior_query = request.GET.get('behavior')
    anticedent_query = request.GET.get('anticedent')
    consequence_query = request.GET.get('consequence')
    function_query = request.GET.get('function')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    qs = student_cases

    if is_valid_queryparam(behavior_query) and behavior_query != 'Choose Behavior':
        qs = qs.filter(Q(behavior__behaviorincident=behavior_query))

    if is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Anticedent':
        qs = qs.filter(Q(anticedent__anticedentincident=anticedent_query))

    if is_valid_queryparam(consequence_query) and consequence_query != 'Choose Consequence':
        qs = qs.filter(Q(consequence__behaviorconsequence=consequence_query))

    if is_valid_queryparam(function_query) and function_query != 'Choose Function':
        qs = qs.filter(Q(function__behaviorfunction=function_query))

    if is_valid_queryparam(date_min):
        qs = qs.filter(Q(date_created__gte=date_min))

    if is_valid_queryparam(date_max):
        qs = qs.filter(Q(date_created__lt=date_max))

    qs_count = qs.count()
    total_beh = student_cases.count()
    beh_devide = (qs_count / total_beh) * 100 if total_beh else None

    context = {
        'queryset': qs,
        'student_cases': student_cases,
        'behaviorset': student.behavior_set.all(),
        'anticedentset': student.anticedent_set.all(),
        'functionset': student.function_set.all(),
        'consequenceset': student.consequence_set.all(),
        'case': Case.objects.all(),
        'qs_count': qs_count,
        'student': student,
        'values': request.GET,
        'total_beh': total_beh,
        'beh_devide': beh_devide
    }

    return render(request, 'bip/filter_data.html', context)








def chart_view(request, pk):    
 
   
    error_message=None
    df = None
    graph = None

 
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'consequence__behaviorconsequence','date_created','time','id')
    
    cases_df = pd.DataFrame(data)
      
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')

    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    
    
    
    df_beh_count = cases_df['Behavior']

    beh_count_graph = get_count_beh_plot( x= df_beh_count, data=cases_df)  
  
  
  
  
    pivot = pd.pivot_table(cases_df,  
                                index='Date', 
                                columns='Behavior', 
                                aggfunc=len,fill_value=0)
    
    trtis = pivot.replace(0, np.nan, inplace=True)
    
    trtis = pivot.reset_index()
    
    
    
    multiple_scater_plot_five = None
    
    try:
        multiple_scater_plot_five= get_multiple_scatter_plot_five(
            x =trtis['Date'], y=trtis.iloc[:,1],data=trtis,
            z=trtis['Date'], k=trtis.iloc[:,2],data1=trtis,
            g=trtis['Date'], q=trtis.iloc[:,3],data2=trtis,
            m=trtis['Date'], n=trtis.iloc[:,4],data3=trtis,
            a=trtis['Date'], b=trtis.ililoc[:,5],data4=trtis


      
        )
           
    except:
        pass
    
    multiple_scater_plot_four = None
    
    try:
        multiple_scater_plot_four= get_multiple_scatter_plot_four(
            x =trtis['Date'], y=trtis.iloc[:,1],data=trtis,
            z=trtis['Date'], k=trtis.iloc[:,2],data1=trtis,
            g=trtis['Date'], q=trtis.iloc[:,3],data2=trtis,
            m=trtis['Date'], n=trtis.iloc[:,4],data3=trtis

      
        )
           
    except:
        pass
    
    multiple_scater_plot_three = None
    try:
    
        multiple_scater_plot_three = get_multiple_scatter_plot_three(
            x =trtis['Date'], y=trtis.iloc[:,1],data=trtis,
            z=trtis['Date'], k=trtis.iloc[:,2],data1=trtis,
            g=trtis['Date'], q=trtis.iloc[:,3],data2=trtis)
           
    except:
        pass
    
    multiple_scater_plot_two = None
    try:
    
        multiple_scater_plot_two = get_multiple_scatter_plot_two(
            x =trtis['Date'], y=trtis.iloc[:,1],data=trtis,
            z=trtis['Date'], k=trtis.iloc[:,2],data1=trtis)
           
    except:
        pass
    
    
    try:
    
        multiple_scater_plot_one = get_multiple_scatter_plot_one(
            x =trtis['Date'], y=trtis.iloc[:,1],data=trtis)
           
    except:
        pass
    
    
    df2 = cases_df['Behavior'].value_counts()
    
    
    pie_graph = get_pie_chart( x=df2, labels=df2.index)
    
    
    
    df3 = cases_df['Anticedent'].value_counts()
    
    pie_anticedent_graph = get_pie__chart_anticedent( x=df3, labels=df3.index)
    
    
    
    
    df4 = cases_df['Function'].value_counts()

    pie_function_graph = get_pie__chart_function( x=df4, labels=df4.index)
    

    df5 = cases_df['Consequence'].value_counts()

    pie_consequence_graph = get_pie__chart_consequence( x=df5, labels=df5.index)
    
    # Duration of behavior
    data_duration = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','duration')
    
    cases_df_duration = pd.DataFrame(data_duration)

    box_duration_graph = None
    
    try:
        duration_behavior = cases_df_duration.groupby('behavior__behaviorincident')['duration'].mean().round(1) 
        
        
        duration_behavior = duration_behavior.to_frame().reset_index()        
        
        
        df_duration = duration_behavior['behavior__behaviorincident']

        # print(df_duration)
        
        dfy_duration = duration_behavior['duration']
        
        # print(dfy_duration)

        
        box_duration_graph = get_duration_bar_chart ( x= df_duration, y= dfy_duration, data=duration_behavior)  
        
        # duration_behavior = duration_behavior.set_index('behavior__behaviorincident')
        
    except:
        
        pass

    

    # correltion table
    
    context = {
        'student':student,
        'beh_count_graph':beh_count_graph,
        'multiple_scater_plot_five':multiple_scater_plot_five,
        'multiple_scater_plot_four':multiple_scater_plot_four,
        'multiple_scater_plot_three':multiple_scater_plot_three,
        'multiple_scater_plot_two':multiple_scater_plot_two,
        'multiple_scater_plot_one':multiple_scater_plot_one,
        'pie_graph':pie_graph,
        'pie_anticedent_graph':pie_anticedent_graph,
        'pie_function_graph':pie_function_graph,
        'pie_consequence_graph':pie_consequence_graph,
        'box_duration_graph':box_duration_graph,

        }
    return render(request, 'bip/chart.html', context)
    

def raw_data(request, pk):



    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    
    data1 = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','consequence__behaviorconsequence','function__behaviorfunction', 'date_created','time','id')

    cases_df_duplicate = pd.DataFrame(data1)
    
    cases_df_duplicate = pd.DataFrame(data1).drop(['time','id','date_created'], axis=1) 
    cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('consequence__behaviorconsequence', 'Consequence')


    # duplicateRows = cases_df_duplicate[cases_df_duplicate[['behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction']].duplicated()== False]
            
    duplicateRows = cases_df_duplicate[cases_df_duplicate.duplicated(['Behavior','Anticedent','Function']) == False].sort_values('Behavior')
          
    behavior_count = cases_df_duplicate['Behavior'].value_counts()

    unique_abcf_count = cases_df_duplicate.groupby(['Behavior','Anticedent','Consequence','Function']).size().reset_index(name='Frequency')





    unique_abcf_count = unique_abcf_count.sort_values(by=['Frequency'], ascending=False)




    unique_abf_count = cases_df_duplicate.groupby(['Behavior','Anticedent','Function']).size().reset_index(name='Frequency')

    unique_abf_count = unique_abf_count.sort_values(by=['Frequency'], ascending=False)

    unique_abc_count = cases_df_duplicate.groupby(['Behavior','Anticedent','Consequence']).size().reset_index(name='Frequency')

    unique_abc_count = unique_abc_count.sort_values(by=['Frequency'], ascending=False)

    unique_ab_count = cases_df_duplicate.groupby(['Behavior','Anticedent']).size().reset_index(name='Frequency')
    unique_ab_count = unique_ab_count.sort_values(by=['Frequency'], ascending=False)

    unique_bf_count = cases_df_duplicate.groupby(['Behavior','Function']).size().reset_index(name='Frequency')
    unique_bf_count = unique_bf_count.sort_values(by=['Frequency'], ascending=False)
  
    # Duration of behavior
    data_duration = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','duration')
    
    cases_df_duration = pd.DataFrame(data_duration)

    box_duration_graph = None

    try:
        duration_behavior = cases_df_duration.groupby('behavior__behaviorincident')['duration'].mean().round(1) 
        
        
        duration_behavior = duration_behavior.to_frame().reset_index()        
        



# df = df.drop('index_column', axis=1)


        df_duration = duration_behavior['behavior__behaviorincident']


    except:
        
        pass


    # Frequency of behavior:

    data_frequency = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','frequency')
    
    cases_df_frequency = pd.DataFrame(data_frequency)

    
    try:

        
        frequency_behavior = cases_df_frequency.groupby('behavior__behaviorincident')['frequency'].mean().round(1) 
        
        
        frequency_behavior = frequency_behavior.to_frame().reset_index()        
        
        
        df_frequency = frequency_behavior['behavior__behaviorincident']

      
        
    except:
        
        pass

    

    # add up the freeuency"


    data_frequency_sum = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','frequency')
    
    cases_df_frequency_sum = pd.DataFrame(data_frequency)


    
    try:

        
        frequency_behavior_sum = cases_df_frequency.groupby('behavior__behaviorincident')['frequency'].sum()


        frequency_behavior_sum = frequency_behavior_sum.to_frame().reset_index()        

        
        frequency_behavior_sum = frequency_behavior_sum.sort_values(by=['frequency'], ascending=False)


        df_frequency_sum= frequency_behavior_sum['behavior__behaviorincident'].sort_values()


    except:
        
        pass

    
    # correaltion
    
    # data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','consequence__behaviorconsequence','function__behaviorfunction', 'date_created','time','id')
    

    cases_df = pd.DataFrame(data1)      
    
    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
    cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
  

    
    behavior = pd.get_dummies(cases_df['Behavior'])
   
    anticedent = pd.get_dummies(cases_df['Anticedent'])


    consequence = pd.get_dummies(cases_df['Consequence'])

    
    function = pd.get_dummies(cases_df['Function'])
    
    
    df_matrix = pd.concat([cases_df,behavior, anticedent, consequence, function], axis=1)
    
    df_matrix.drop(['Behavior','Anticedent','Function', 'Consequence','Date','Time','ID'],axis=1,inplace=True)
        
    matrix = df_matrix.corr().round(2) 

  
# end correlation

    context = {
        'student':student,
        'unique_abcf_count':unique_abcf_count.to_html(),
        'unique_abc_count':unique_abc_count.to_html(),
        'unique_abf_count':unique_abf_count.to_html(),
        'unique_bf_count':unique_bf_count.to_html(),
        'duplicateRows':duplicateRows.to_html(),
        'unique_ab_count':unique_ab_count.to_html(),

        # 'duration_behavior':duration_behavior.to_html(),
        'frequency_behavior':frequency_behavior.to_html(),

        'frequency_behavior_sum':frequency_behavior_sum.to_html(),
        'matrix':matrix.to_html(),





       

        }

    return render(request, 'bip/raw_data.html', context)


def export(request,pk):



    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    
    writer.writerow(["Case","Behavior", "Antecedent","Consequence","Function", "Duration(Sec)","Date"])
    
    for case in  Case.objects.filter(student__id=pk).values_list('student__studentname','behavior__behaviorincident','anticedent__anticedentincident','consequence__behaviorconsequence','function__behaviorfunction','duration','date_created'):
        writer.writerow(case)    

    
    response['Content-Disposition'] = 'attachment; filename= "FBA Data.csv"'
    
    
    return response




# donwload to word xxxxxxx

def download_webpage_to_word(request, url):
    decoded_url = unquote(url)

    # Add schema if missing
    if not decoded_url.startswith(('http://', 'https://')):
        decoded_url = 'http://' + decoded_url

    response = requests.get(decoded_url)

    if response.status_code == 200:
        # Convert HTML to plain text, except for tables
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.skip_internal_links = True
        content_text = h.handle(response.text)

        document = Document()
        document.add_paragraph(content_text)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="webpage.docx"'
        document.save(response)

        return response
    else:
        return HttpResponse(f"Failed to fetch the webpage: {response.status_code}")
    
def download_page(request):
    return render(request, 'bip/download_page.html')





# LEFT OFFF August 9th
def assign_data_entry(request, pk):
  
    student = get_object_or_404(Student, pk=pk)
    
    student_behaviors = student.case_set.all() 
        
    behavior = Behavior.objects.all()

    casemanager = models.CaseManager.objects.all()

    case = Case.objects.all()

    studentcurrent = Student.objects.get(id=pk)

    # check this after ereasing the data 11/6
    # user = User.objects.get(id=pk)

          
    context = {
    'student_behaviors':student_behaviors,
    "student":student,
    'case':case,
    # 'user':user,
    
               }
    
    
    return render(request, 'bip/assign_data_entry.html',context, )
    
def create_unique_id(request, pk):
        
    studentupdate = Student.objects.get(id=pk)

    form = StudentFormSlug(instance=studentupdate)
    
    if request.method == 'POST': 
      form = StudentFormSlug(request.POST, instance=studentupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:dashboard", studentupdate.id)
    
   
    context = {'form':form}
    
    return render(request, "bip/create_id.html", context)



def updateunique_case_identifier(request, pk):
        
    studentupdate = Student.objects.get(id=pk)

    form = StudentFormSlug(instance=studentupdate)
    
    if request.method == 'POST': 
      form = StudentFormSlug(request.POST, instance=studentupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:assign_data_entry", studentupdate.id)
    
   
    context = {'form':form}
    
    return render(request, "bip/create_student.html", context)


def case_manager_unique_identifier(request, pk):
    
    userupdate = models.CaseManager.objects.get(id=pk)

    form = UpdateCaseManagerForm(instance=userupdate)
    
    if request.method == 'POST': 
      form = UpdateCaseManagerForm(request.POST, instance=userupdate) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user
          
          instance.save()  
          
          return redirect("bip:for_user", userupdate.user)
    
   
    context = {'form':form}
    
    return render(request, "bip/case_manager_unique_identifier.html", context)
