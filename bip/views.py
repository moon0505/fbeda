from django.shortcuts import render, redirect, get_object_or_404 
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.urls import reverse
from bip import models
from django.urls import reverse_lazy
import logging
from django.contrib.auth.models import User 
from . import forms
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from bip.forms import CaseManagerUserForm, CaseManagerForm,CsvUploadForm
from datetime import datetime
from django.contrib.auth import views as auth_views

from django.utils import timezone
import datetime

from django.db import IntegrityError
from django import template
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.contrib.auth.decorators import login_required,user_passes_test
from .models import   Student, Behavior, Case, Anticedent, Function, Consequence,Enviroment,CustomUser
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
    get_box_plot_time,
    get_intensity_bar_chart,
    get_heatmap_antecedent,
    get_clustermap_antecedent, 
    get_clustermap_function,
    get_heatmap_function,
    get_heatmap_consequence,
    get_clustermap_consequence,
    get_heatmap_setting,
    get_clustermap_setting

    )


import pandas as pd
import numpy as np
import csv,io
from django.contrib import messages 
import requests
from docx import Document
from django.shortcuts import render
from urllib.parse import unquote
import html2text




def luna(request):
    
    return render(request,'bip/luna.html')


def statistics(request,pk):
    student = get_object_or_404(Student, pk=pk)
    student_behaviors = student.case_set.all()
    

    context = {
    'student_behaviors': student_behaviors,
    "student":student,
    
    }
    return render(request,'bip/statistics.html',context)



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
def case_manager_dashboard_view(request,pk):
    
    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)

    specific_data_entry =models.DataEntry.objects.filter(assignedCaseManagerSlug=case_manager_entry.slug)

    

    mydict={
        'specific_data_entry':specific_data_entry,
        # 'data_entry':data_entry,
        # 'data_entry_hold':data_entry_hold
   
    }
    return render(request,'account/case_manager_dashboard.html',context=mydict)

@login_required(login_url='data_entry_login')
@user_passes_test(is_data_entry)
def data_entry_dashboard_view(request):
    
    data_entry =models.DataEntry.objects.get(user_id=request.user.id)
    case_manager=models.CaseManager.objects.get(slug=data_entry.assignedCaseManagerSlug)
    
    assigned_student =models.Student.objects.get(slug=data_entry.assignedStudentSlug)
 
    unique_behaviors = assigned_student.behavior_set.values('behaviorincident', 'behavior_definition','intensity_definition').distinct()


    mydict={
    'data_entry':data_entry,
    'unique_behaviors':unique_behaviors,
    'case_manager':case_manager,
    'case_manager_name':case_manager.get_name,
    'assigned_student':assigned_student,
    
    }
    return render(request,'account/data_entry_dashboard.html',context=mydict)

@login_required(login_url='data_entry_login')
@user_passes_test(is_data_entry)
def data_entry_input_view(request, pk):
  
    student = get_object_or_404(Student, pk=pk)
    student_behaviors = student.case_set.all()[:15] 
    behavior = Behavior.objects.all()
    case = Case.objects.all()



    student_time = student.case_set.filter(time__isnull=False).first()
    student_duration = student.case_set.filter(duration__isnull=False).first()
    student_enviroment = student.case_set.filter(enviroment__isnull=False).first()

      
    # this works:
    stbehavior = student.behavior_set.all() 
    
        
    behaivorpest  = behavior.filter(pk=pk).filter(behaviorincident__icontains="behaviorincident")
    
    context = {'student_behaviors':student_behaviors,
               "student":student,
               "student_time":student_time,
                "student_duration":student_duration,
                'student_enviroment':student_enviroment,

               }
     
    return render(request, 'bip/data_entry_input.html',context, )



@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def admin_approve_data_entry_view(request,pk):
    #those whose approval are needed
    # case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)
    
    # specific_data_entry =models.DataEntry.objects.get(assignedCaseManagerSlug=case_manager_entry.pk)
    
    specific_data_entry=models.DataEntry.objects.all().filter(status=False)

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

    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)

    return redirect('bip:case_manager_dashboard',case_manager_entry.id)

@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)

def admin_delete_data_entry_view(request,pk):
    # case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)
    # specific_data_entry =models.DataEntry.objects.get(assignedCaseManagerSlug=case_manager_entry.slug)
    specific_data_entry=models.DataEntry.objects.get(id=pk)


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

    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)

    return redirect('bip:case_manager_dashboard',case_manager_entry.id)


@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)
def reject_data_entry_view(request,pk):
    data_entry=models.DataEntry.objects.get(id=pk)
    user=models.User.objects.get(id=data_entry.user_id)
    user.delete()
    data_entry.delete()
    case_manager_entry =models.CaseManager.objects.get(user_id=request.user.id)

    return render(request,'bip/welcome_user.html')

# Website forms/input---------------------------------------------------------

class UserPosts(LoginRequiredMixin, generic.ListView):
    model = models.Student
    template_name = "bip/student_list.html"

    def get_queryset(self):
        try:
            self.post_user = CustomUser.objects.prefetch_related("postts").get(
                username__iexact=self.kwargs.get("username")
            )
        except CustomUser.DoesNotExist:
            raise Http404
        else:
            return self.post_user.postts.all()


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'bip/welcome_user.html'


@login_required
def list_view(request,pk):
    
    user = get_object_or_404(User, pk=pk)
    user_list = user.case_set.all()
    context ={'user ':user,'user_list':user_list}  
         
    return render(request, "bip/preffered_student_list.html", context)

@login_required(login_url='case_manager_login')
@user_passes_test(is_case_manager)

def dashboard(request, pk):
  
    student = get_object_or_404(Student, pk=pk)
    student_behaviors = student.case_set.all()
    student_time = student.case_set.filter(time__isnull=False).first()
    student_duration = student.case_set.filter(duration__isnull=False).first()
    student_enviroment = student.case_set.filter(enviroment__isnull=False).first()

    

    context = {
    'student_behaviors': student_behaviors,
    "student":student,
    'student_time':student_time,  
    'student_duration':student_duration,  
    'student_enviroment':student_enviroment,        
    }
    
    return render(request, 'bip/dashboard.html',context, )


@login_required
def behavior_form_view(request, pk):

    student = Student.objects.get(id=pk) 
    student_cases = student.case_set.all() 
    student_behaviors = student.case_set.all()

    behaviorset = student.behavior_set.all()

    

    anticedentset = student.anticedent_set.all()
    functionset = student.function_set.all()
    consequset = student.consequence_set.all()
    enviromentset = student.enviroment_set.all()

    unique_behaviors = student.behavior_set.values('behaviorincident', 'behavior_definition').distinct()


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

        
    return render(request, 'bip/fbo_form.html', {'form': form,'student':student,'student_cases':student_cases,'unique_behaviors':unique_behaviors})


@login_required      
def updatePost(request, pk,student_id ):
    
    student_post = Case.objects.get(id=pk, student_id= student_id) 
    form = BehaviorForm(instance=student_post)
    
   # Filter behaviors related to the specific student or pk
    behaivorpest = Behavior.objects.filter(student_id=student_id)
    anticedentpest = Anticedent.objects.filter(student_id=student_id)
    functionpest = Function.objects.filter(student_id=student_id)
    consequenceset = Consequence.objects.filter(student_id=student_id)
    enviromentset = Enviroment.objects.filter(student_id=student_id)

        
    if request.method == 'POST': 
      form = BehaviorForm(request.POST, instance=student_post) 
      
      if form.is_valid():
          instance = form.save(commit=False)
          instance.user = request.user 
          
          instance.save()  
          
          


          if is_case_manager(request.user):
                return redirect("bip:dashboard", student_post.student.id)

          elif is_data_entry(request.user):
                return redirect("bip:data_entry_input", student_post.student.id)
    
    else:
        form = BehaviorForm(instance=student_post)                                           
        form.fields["behavior"].queryset=behaivorpest
        form.fields["anticedent"].queryset=anticedentpest
        form.fields["function"].queryset=functionpest
        form.fields["consequence"].queryset=consequenceset
        form.fields["enviroment"].queryset=enviromentset


    
    context = {'form':form,
            'student_post':student_post,
               }
    
    return render(request, "bip/update_post.html", context)


def deletePost(request, pk):
  behavior_incident = Case.objects.get(id=pk)
  
  if request.method == 'POST': 
    behavior_incident.delete()

    if is_case_manager(request.user):
                return redirect("bip:dashboard", behavior_incident.student.id)

    elif is_data_entry(request.user):
                return redirect("bip:data_entry_input", behavior_incident.student.id)
    
  
  context = {'incident': behavior_incident}
  return render(request, 'bip/delete_post.html', context)


def create_student(request):
    
    user_student = CustomUser.objects.get(pk=request.user.id)
    form = StudentForm()
    if  is_case_manager(request.user):

            if request.method == 'POST':
                if request.user.is_authenticated:
                    form = StudentForm(request.POST)   
                    
                    for field in form:
                        print(field.value())
                    
                    if form.is_valid():
                        obj = form.save(commit=False)
                        obj.user_student = CustomUser.objects.get(pk=request.user.id)
                        obj.save()                 
                        
                        return redirect("bip:for_user", username=request.user.username)
                        
                    else:
                        print("ERROR In Form") 
                        
            
            return render(request, 'bip/create_student.html', {'form': form,'user_student':user_student})
    else :
        return redirect("bip:data_entry_dashboard")
    
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


def deleteUser(request, pk):
    user_delete= CustomUser.objects.get(pk=request.user.id)

    user = CustomUser.objects.get(id=pk)
    
    if request.method == "POST":
        user_delete.delete()
        return redirect("bip:description")
    
    context = {'item':user_delete,'user':user}
    return render(request, "bip/delete_user.html", context)



def user_account(request, pk):
    user_account= CustomUser.objects.get(pk=request.user.id)
    user = CustomUser.objects.get(id=pk)

    context = {'user_account':user_account,'user':user}

    return render(request,'bip/user_account.html')





def create_behavior(request,pk):
    user = CustomUser.objects.get(pk=request.user.id)
    student = Student.objects.get(id=pk) 

    form = CreateBehaviorForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateBehaviorForm(request.POST)
            
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = CustomUser.objects.get(pk=request.user.id)
                 obj.student = student
                 obj.save()
                 return redirect("bip:dashboard", student.id)                
                      
            else:
                print("ERROR In Form") 
            
    return render(request, 'bip/create_behavior.html', {'form': form})


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
    
    if request.method == "POST":
        behdelete.delete()
        return redirect("bip:dashboard", behdelete.student.id)
    
    context = {'item':behdelete}
    return render(request, "bip/delete_behavior.html", context)

@login_required
def create_anticedent(request,pk):
    user = CustomUser.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateAnticedentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateAnticedentForm(request.POST)

            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = CustomUser.objects.get(pk=request.user.id)
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
          return redirect("bip:edit_anticedent", antiupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_anticedent.html", context)


def deleteAnticedent(request, pk):
    antidelete = Anticedent.objects.get(id=pk)
    
    if request.method == "POST":
        antidelete.delete()
        return redirect("bip:dashboard", antidelete.student.id)
    
    context = {'item':antidelete}
    return render(request, "bip/delete_anticedent.html", context)


@login_required
def create_function(request,pk):
    user = CustomUser.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateFunctionForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateFunctionForm(request.POST)
        
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = CustomUser.objects.get(pk=request.user.id)
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
          
          return redirect("bip:edit_function", funcupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_function.html", context)


def deleteFunction(request, pk):  
    funcdelete = Function.objects.get(id=pk)    
    if request.method == "POST":
        funcdelete.delete()
        return redirect("bip:dashboard", funcdelete.student.id)
    
    context = {'item':funcdelete}
    return render(request, "bip/delete_function.html", context)


@login_required
def create_consequence(request,pk):
    user = CustomUser.objects.get(pk=request.user.id)
    
    student = Student.objects.get(id=pk) 

    form = CreateConsequenceForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateConsequenceForm(request.POST)

            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = CustomUser.objects.get(pk=request.user.id)
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
          
          return redirect("bip:edit_consequence", conqupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_consequence.html", context)


def deleteConsequence(request, pk): 
    conqdelete = Consequence.objects.get(id=pk)
    if request.method == "POST":
        conqdelete.delete()
        return redirect("bip:dashboard", conqdelete.student.id)
    
    context = {'item':conqdelete}
    return render(request, "bip/delete_consequence.html", context)

@login_required
def create_setting_view(request,pk):
    user = CustomUser.objects.get(pk=request.user.id) 
    student = Student.objects.get(id=pk) 

    form = CreateEnviromentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateEnviromentForm(request.POST)
        
            for field in form:
                print(field.value())
            
            if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user = CustomUser.objects.get(pk=request.user.id)
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
          
          return redirect("bip:edit_setting", enviromentupdate.student.id)
    context = {'form':form}
    
    return render(request, "bip/create_setting.html", context)

def deleteEnviroment(request, pk):
    envdelete = Enviroment.objects.get(id=pk)
    if request.method == "POST":
        envdelete.delete()
        return redirect("bip:dashboard", envdelete.student.id)
    
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

# correaltion
def correlation_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident',
                                                             'anticedent__anticedentincident',
                                                             'function__behaviorfunction', 'date_created','time','id')
    cases_df = pd.DataFrame(data)



    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')

        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)

    

    # cluster heatmapcorrelation matrixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    behavior = pd.get_dummies(cases_df['Behavior'])
    anticedent = pd.get_dummies(cases_df['Anticedent'])
    function = pd.get_dummies(cases_df['Function'])
    df_matrix = pd.concat([cases_df,behavior, anticedent,function], axis=1)
    df_matrix.drop(['Behavior','Anticedent','Function', 'Date','Time','ID'],axis=1,inplace=True)
    matrix = df_matrix.corr().round(2) 
    
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
    iheat_graph = None
    
    try:
        iheat_graph = get_heatmap(data=matrix)

    except:
        pass


    context = {
        'student':student,
        'iclustermap_graph':iclustermap_graph,
        'iheat_graph':iheat_graph,


    }

    return render(request, 'bip/correlation.html', context)

def pie_chart_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'consequence__behaviorconsequence','id')
    cases_df = pd.DataFrame(data)
    try:
        
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')

        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)

    # pie chartxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    df2 = cases_df['Behavior'].value_counts()
    pie_graph = get_pie_chart( x=df2, labels=df2.index)
    df3 = cases_df['Anticedent'].value_counts()
    pie_anticedent_graph = get_pie__chart_anticedent( x=df3, labels=df3.index)
    df4 = cases_df['Function'].value_counts()
    pie_function_graph = get_pie__chart_function( x=df4, labels=df4.index)
    df5 = cases_df['Consequence'].value_counts()
    pie_consequence_graph = get_pie__chart_consequence( x=df5, labels=df5.index)


    context= {
    
        'student':student,
        'pie_graph':pie_graph,
        'pie_anticedent_graph':pie_anticedent_graph,
        'pie_function_graph':pie_function_graph,
        'pie_consequence_graph':pie_consequence_graph,
    }

    return render(request, 'bip/pie_charts.html', context)




def snapshot_view(request, pk):
    error_message=None
    df = None
    graph = None
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','consequence__behaviorconsequence','function__behaviorfunction', 'date_created','time','id')
    cases_df = pd.DataFrame(data)

    # beging time

    cases_df_time = None

    box_graph_time = None

    try:

        cases_df_time= pd.DataFrame(data).drop(['id',], axis=1) 

        # cases_df_time['combined_datetime'] = pd.to_datetime(cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str), format='%H:%M:%S')
        cases_df_time['combined_datetime'] = pd.to_datetime(cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str))


        cases_df_time.columns = cases_df_time.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df_time.columns = cases_df_time.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df_time.columns = cases_df_time.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df_time.columns = cases_df_time.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df_time.columns = cases_df_time.columns.str.replace('enviroment__behaviorenviroment', 'Setting')
        
        cases_df_time['hour_12h'] = cases_df_time['combined_datetime'].dt.strftime('%I %p')

        cases_df_time = cases_df_time.sort_values('hour_12h')

        df_time = cases_df_time['hour_12h']

        # sort get_box_plot_time x axis to be in order from earliest time 
        box_graph_time = get_box_plot_time( x= df_time, data=cases_df_time) 
 
    except:
        pass
# ending time
    

    # duration begiing
    data_duration = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','duration')
    cases_df_duration = pd.DataFrame(data_duration)

    box_duration_graph = None
    
    try:
        duration_behavior = cases_df_duration.groupby('behavior__behaviorincident')['duration'].mean().round(1) 
        duration_behavior = duration_behavior.to_frame().reset_index()        
        df_duration = duration_behavior['behavior__behaviorincident']
        dfy_duration = duration_behavior['duration']
      
        box_duration_graph = get_duration_bar_chart ( x= df_duration, y= dfy_duration, data=duration_behavior)  
                
    except:
        
        pass




     # intensity charts
    
    data_intensity = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','intensity')
    cases_df_intensity= pd.DataFrame(data_intensity)

    # intensitiy formula:
    box_intensity_graph = None
    
    try:
        intensity_behavior = cases_df_intensity.groupby('behavior__behaviorincident')['intensity'].mean().round(1) 
        intensity_behavior = intensity_behavior.to_frame().reset_index()        
        df_intensity = intensity_behavior['behavior__behaviorincident']
        dfy_intensity = intensity_behavior['intensity']
      
        box_intensity_graph = get_intensity_bar_chart ( x= df_intensity, y= dfy_intensity, data=intensity_behavior)  
                
    except:
        
        pass


    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')

        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)

    df1 = cases_df['Date'].value_counts()
    df1 = df1.to_frame().reset_index() 
    df2 = df1.reset_index()
    df2 = df2.sort_values(by=['index'])
    df3 = df2['Date']
    df4 = df2['count']

    bar_graph = get_bar_chart(x=df3, y = df4)
  

    df_beh_count = cases_df['Behavior']
    beh_count_graph = get_count_beh_plot( x= df_beh_count, data=cases_df)  


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
        # print("Selected y column is empty or does not exist.")
        pass
  


    
    context= {
    
        'student':student,
        'bar_graph':bar_graph,
        'beh_count_graph':beh_count_graph,
        'multiple_line_plot_one':multiple_line_plot_one,
        'multiple_line_plot_two':multiple_line_plot_two,
        'multiple_line_plot_three':multiple_line_plot_three,
        'multiple_line_plot_four':multiple_line_plot_four,
        'multiple_line_plot_five':multiple_line_plot_five, 
        'multiple_line_plot_chatgpt':multiple_line_plot_chatgpt,
        'box_graph_time':box_graph_time,
        'box_duration_graph':box_duration_graph,
        'box_intensity_graph':box_intensity_graph,

    }
    


    return render(request, 'bip/snapshot.html', context)


def snapshot_data_entry_view(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    data = models.Case.objects.filter(student__id=pk).values(
    'behavior__behaviorincident', 'anticedent__anticedentincident', 'function__behaviorfunction',
    'consequence__behaviorconsequence', 'enviroment__behaviorenviroment', 'date_created', 'time', 
    'duration', 'id'
)

    # Creating DataFrame
    cases_df = pd.DataFrame(data)

    # Renaming the columns
    rename_columns = {
        'behavior__behaviorincident': 'Behavior',
        'anticedent__anticedentincident': 'Antecedent',
        'function__behaviorfunction': 'Function',
        'consequence__behaviorconsequence': 'Consequence',
        'enviroment__behaviorenviroment': 'Setting',
        'date_created': 'Date',
        'time': 'Time',
        'duration': 'Duration',
        'id': 'ID'
    }
    cases_df.rename(columns=rename_columns, inplace=True)

    # Checking for empty columns and dropping them
    empty_columns = [col for col in ['Duration', 'Setting', 'Time'] if cases_df[col].isna().all()]
    cases_df.drop(columns=empty_columns, inplace=True, errors='ignore')

    # Final DataFrame for the table
    table_df = cases_df.drop(['ID'], axis=1) 



    



    df1 = cases_df['Date'].value_counts()
    df1 = df1.to_frame().reset_index() 
    df2 = df1.reset_index()
    df2 = df2.sort_values(by=['index'])
    df3 = df2['Date']
    df4 = df2['count']

    bar_graph = get_bar_chart(x=df3, y = df4)
  


    df_beh_count = cases_df['Behavior']
    beh_count_graph = get_count_beh_plot( x= df_beh_count, data=cases_df)  


    # multiple bar graph



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
        # print("Selected y column is empty or does not exist.")
        pass

        # pie charts


    df2 = cases_df['Behavior'].value_counts()
    pie_graph = get_pie_chart( x=df2, labels=df2.index)
    df3 = cases_df['Antecedent'].value_counts()
    pie_anticedent_graph = get_pie__chart_anticedent( x=df3, labels=df3.index)
    df4 = cases_df['Function'].value_counts()
    pie_function_graph = get_pie__chart_function( x=df4, labels=df4.index)
    df5 = cases_df['Consequence'].value_counts()
    pie_consequence_graph = get_pie__chart_consequence( x=df5, labels=df5.index)


    context= {
    
        'student':student,
        'table_df':table_df.to_html(),
        'bar_graph':bar_graph,
        'beh_count_graph':beh_count_graph,
        'multiple_line_plot_one':multiple_line_plot_one,
        'multiple_line_plot_two':multiple_line_plot_two,
        'multiple_line_plot_three':multiple_line_plot_three,
        'multiple_line_plot_four':multiple_line_plot_four,
        'multiple_line_plot_five':multiple_line_plot_five, 
        'pie_graph':pie_graph,
        'pie_anticedent_graph':pie_anticedent_graph,
        'pie_function_graph':pie_function_graph,
        'pie_consequence_graph':pie_consequence_graph,
       
    }
    
    return render(request, 'bip/data_entry_chart_view.html', context)

# xxxxxxxx

def function_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    
    cases_df = pd.DataFrame(data)
    
    try:

        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
        
    except:
        return redirect("bip:error_page", student.id)


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
    
        iheat_graph_function = get_heatmap_function(data=filterDX)
    except:
        pass
    

    iclustermap_graph = None
    
    try:
        iclustermap_graph_function = get_clustermap_function(data=matrix)

    except:
        pass
  
    context= {'student':student,
              'iclustermap_graph_function':iclustermap_graph_function, 
    'iheat_graph_function':iheat_graph_function, 
    'box_graph_function':box_graph_function,}
    
    return render(request, 'bip/function.html', context)


def consequence_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'consequence__behaviorconsequence','date_created','time','id')
    cases_df = pd.DataFrame(data)
    
    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)

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

    try:
        filterDX = matrix[((matrix > 0.0)) & (matrix != 1.000)]
    
        iheat_graph_consequence = get_heatmap_consequence(data=filterDX)
    except:
        pass

    iclustermap_graph_consequence = None
    
    try:
        iclustermap_graph_consequence = get_clustermap_consequence(data=matrix)

    except:
        pass

    context= {'student':student,
              'iclustermap_graph_consequence':iclustermap_graph_consequence, 
    'iheat_graph_consequence':iheat_graph_consequence, 
    'box_graph_consequence':box_graph_consequence,}
    
    return render(request, 'bip/consequence.html', context)


def anticedent_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'date_created','time','id')
    cases_df = pd.DataFrame(data)
      
    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)


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
    
        iheat_graph_antecedent = get_heatmap_antecedent(data=filterDX)
    except:
        pass
    iclustermap_graph_antecedent = None
    
    try:
        iclustermap_graph_antecedent = get_clustermap_antecedent(data=filterDX)

    except:
        pass
  
  
    context= {'student':student,
              'iclustermap_graph_antecedent':iclustermap_graph_antecedent, 
    'iheat_graph_antecedent':iheat_graph_antecedent, 
    'box_graph':box_graph,}
    
    
    return render(request, 'bip/anticedent.html', context)

# Setting enviroment
def enviroment_view(request,pk):
     
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'enviroment__behaviorenviroment','date_created','time','id')
    cases_df = pd.DataFrame(data)   

    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('enviroment__behaviorenviroment', 'Enviroment')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
    except:
        return redirect("bip:error_page", student.id)

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
    
        iheat_graph_setting = get_heatmap_setting(data=filterDX)
    except:
        pass
    

    iclustermap_graph_setting = None
    
    try:
        iclustermap_graph_setting = get_clustermap_setting(data=matrix)

    except:
        pass
  
  
    context= {'student':student,
        'iclustermap_graph_setting':iclustermap_graph_setting, 
    'iheat_graph_setting':iheat_graph_setting, 
    'box_graph_setting':box_graph_setting,}
    
    
    return render(request, 'bip/setting.html', context)


# end of enviroment setting

def is_valid_queryparam(param):
    return param != '' and param is not None


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

    if is_valid_queryparam(anticedent_query) and anticedent_query != 'Choose Antecedent':
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
    cases_df_time = None
    box_graph_time = None
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    
    data = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','function__behaviorfunction', 'consequence__behaviorconsequence','date_created','time','id')
    
    try:
    # beging time
        cases_df_time= pd.DataFrame(data).drop(['id',], axis=1) 
        cases_df_time['combined_datetime'] = pd.to_datetime(cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str))
        # cases_df_time['combined_datetime'] = pd.to_datetime(cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str), format='%H:%M:%S')

        cases_df_time.columns = cases_df_time.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df_time.columns = cases_df_time.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df_time.columns = cases_df_time.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df_time.columns = cases_df_time.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df_time.columns = cases_df_time.columns.str.replace('enviroment__behaviorenviroment', 'Setting')
        
        cases_df_time['hour_12h'] = cases_df_time['combined_datetime'].dt.strftime('%I %p')



        cases_df_time = cases_df_time.sort_values('hour_12h')

        df_time = cases_df_time['hour_12h']

        # sort get_box_plot_time x axis to be in order from earliest time 
        box_graph_time = get_box_plot_time( x= df_time, data=cases_df_time) 

    except:
        pass
# ending time

    cases_df = pd.DataFrame(data)
      
    try:
        cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Anticedent')
        cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
        cases_df.columns = cases_df.columns.str.replace('time', 'Time')
        cases_df.columns = cases_df.columns.str.replace('id', 'ID')
        
    except:
        return redirect("bip:error_page", student.id)

    
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

    data_duration = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','duration')
    cases_df_duration = pd.DataFrame(data_duration)

    box_duration_graph = None
    
    try:
        duration_behavior = cases_df_duration.groupby('behavior__behaviorincident')['duration'].mean().round(1) 
        duration_behavior = duration_behavior.to_frame().reset_index()        
        df_duration = duration_behavior['behavior__behaviorincident']
        dfy_duration = duration_behavior['duration']
      
        box_duration_graph = get_duration_bar_chart ( x= df_duration, y= dfy_duration, data=duration_behavior)  
                
    except:
        
        pass

    data_intensity = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','intensity')
    cases_df_intensity= pd.DataFrame(data_intensity)

    # intensitiy formula:
    box_intensity_graph = None
    
    try:
        intensity_behavior = cases_df_intensity.groupby('behavior__behaviorincident')['intensity'].mean().round(1) 
        intensity_behavior = intensity_behavior.to_frame().reset_index()        
        df_intensity = intensity_behavior['behavior__behaviorincident']
        dfy_intensity = intensity_behavior['intensity']
      
        box_intensity_graph = get_intensity_bar_chart ( x= df_intensity, y= dfy_intensity, data=intensity_behavior)  
                
    except:
        
        pass

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
        'box_graph_time':box_graph_time,
        'box_intensity_graph':box_intensity_graph,
        }
    return render(request, 'bip/chart.html', context)
    

def raw_data(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    data1 = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','anticedent__anticedentincident','consequence__behaviorconsequence','function__behaviorfunction', 'enviroment__behaviorenviroment','date_created','time','id')

    unique_hour_html = None
    try:
        cases_df_time= pd.DataFrame(data1).drop(['id',], axis=1) 
        # made this correction on 12/31/2023
        cases_df_time['combined_datetime'] = pd.to_datetime(
            cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str),
            format='%Y-%m-%d %H:%M:%S'
                )
        
        # cases_df_time['combined_datetime'] = pd.to_datetime(cases_df_time['date_created'].astype(str) + ' ' + cases_df_time['time'].astype(str))

        # cases_df_time= pd.DataFrame(data1).drop(['time','date_created'], axis=1) 

        cases_df_time.columns = cases_df_time.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df_time.columns = cases_df_time.columns.str.replace('anticedent__anticedentincident', 'Antecedent')
        cases_df_time.columns = cases_df_time.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df_time.columns = cases_df_time.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df_time.columns = cases_df_time.columns.str.replace('enviroment__behaviorenviroment', 'Setting')

        cases_df_time['Hour'] = cases_df_time['combined_datetime'].dt.strftime('%I %p')

    # Group by 'Behavior' and 'hour_12h' to count frequency
        unique_hour = cases_df_time.groupby(['Behavior', 'Hour']).size().reset_index(name='Frequency')
        unique_hour = unique_hour.sort_values(by='Frequency', ascending=False)

        unique_hour_html = unique_hour.to_html(index=False)
    except:
        pass

    cases_df_duplicate = pd.DataFrame(list(data1))

# Reset the index of the DataFrame

    try:
        cases_df_duplicate = pd.DataFrame(data1).drop(['time','id','date_created'], axis=1) 
    
        cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('behavior__behaviorincident', 'Behavior')
        cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('anticedent__anticedentincident', 'Antecedent')
        cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('function__behaviorfunction', 'Function')
        cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
        cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('enviroment__behaviorenviroment', 'Setting')
    except:
        return redirect("bip:error_page", student.id)

    duplicateRows = cases_df_duplicate[cases_df_duplicate.duplicated(['Behavior','Antecedent','Function',]) == False].sort_values('Behavior')
    behavior_count = cases_df_duplicate['Behavior'].value_counts()
    unique_b_count = cases_df_duplicate.groupby(['Behavior']).size().reset_index(name='Frequency')
    unique_b_count = unique_b_count.sort_values(by=['Frequency'], ascending=False)
    unique_abcf_count = cases_df_duplicate.groupby(['Behavior','Antecedent','Consequence','Function']).size().reset_index(name='Frequency')
    unique_abcf_count = unique_abcf_count.sort_values(by=['Frequency'], ascending=False)
    unique_abf_count = cases_df_duplicate.groupby(['Behavior','Antecedent','Function']).size().reset_index(name='Frequency')
    unique_abf_count = unique_abf_count.sort_values(by=['Frequency'], ascending=False)
    unique_abc_count = cases_df_duplicate.groupby(['Behavior','Antecedent','Consequence']).size().reset_index(name='Frequency')
    unique_abc_count = unique_abc_count.sort_values(by=['Frequency'], ascending=False)
    unique_ab_count = cases_df_duplicate.groupby(['Behavior','Antecedent']).size().reset_index(name='Frequency')
    unique_ab_count = unique_ab_count.sort_values(by=['Frequency'], ascending=False)
    unique_bf_count = cases_df_duplicate.groupby(['Behavior','Function']).size().reset_index(name='Frequency')
    unique_bf_count = unique_bf_count.sort_values(by=['Frequency'], ascending=False)
    
    unique_bs_count = cases_df_duplicate.groupby(['Behavior','Setting']).size().reset_index(name='Frequency')
    unique_bs_count = unique_bs_count.sort_values(by=['Frequency'], ascending=False)


    # Duration of behavior

    
    
    duration_html = None
    try: 
        data_duration = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident', 'duration')
        cases_df_duration = pd.DataFrame(data_duration)

# Rename columns
        cases_df_duration = cases_df_duration.rename(columns={'behavior__behaviorincident': 'Behavior', 'duration': 'Duration'})

# Group and calculate the mean duration
        duration_behavior = cases_df_duration.groupby('Behavior')['Duration'].mean().round(0).astype(int).reset_index()

# Extract the 'Behavior' column
        df_duration = duration_behavior['Behavior']

# Convert the DataFrame to HTML
        duration_html = duration_behavior.to_html(index=False)
        
    except:
        
        pass

    # intenity chart


    intensity_html = None
    try: 
        data_intensity = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident', 'intensity')
        cases_df_intensity = pd.DataFrame(data_intensity)

# Rename columns
        cases_df_intensity = cases_df_intensity.rename(columns={'behavior__behaviorincident': 'Behavior', 'intensity': 'Intensity'})

# Group and calculate the mean duration
        # intensity_behavior = cases_df_intensity.groupby('Behavior')['Intensity'].mean().round(0).astype(int).reset_index()
        intensity_behavior = cases_df_intensity.groupby('Behavior')['Intensity'].mean().round(2).reset_index()


# Extract the 'Behavior' column
        df_intensity = intensity_behavior['Behavior']

# Convert the DataFrame to HTML
        intensity_html = intensity_behavior.to_html(index=False)
        
    except:
        
        pass


    # Frequency of behavior:

    data_frequency = models.Case.objects.filter(student__id=pk).values('behavior__behaviorincident','frequency')
    cases_df_frequency = pd.DataFrame(data_frequency)

# Rename columns with 'enviroment__behaviorenviroment' to 'Setting'
    cases_df_duplicate.columns = cases_df_duplicate.columns.str.replace('enviroment__behaviorenviroment', 'Setting')

    try:
    # Group and calculate the mean frequency
        # frequency_behavior = cases_df_frequency.groupby('behavior__behaviorincident')['frequency'].mean().round(0).astype(int).reset_index()
        frequency_behavior = cases_df_frequency.groupby('behavior__behaviorincident')['frequency'].mean().round(2).astype(int).reset_index()

    
    # Rename the 'behavior__behaviorincident' column to 'Behavior'
        frequency_behavior = frequency_behavior.rename(columns={'behavior__behaviorincident': 'Behavior', 'frequency': 'Frequency'})

        
    
    # Extract the 'Behavior' column
        df_frequency = frequency_behavior['Behavior']
    except:
        pass




    cases_df = pd.DataFrame(data1)      
    cases_df = pd.DataFrame(data1).drop(['enviroment__behaviorenviroment'], axis=1) 

    cases_df.columns = cases_df.columns.str.replace('behavior__behaviorincident', 'Behavior')
    cases_df.columns = cases_df.columns.str.replace('anticedent__anticedentincident', 'Antecedent')
    cases_df.columns = cases_df.columns.str.replace('consequence__behaviorconsequence', 'Consequence')
    cases_df.columns = cases_df.columns.str.replace('function__behaviorfunction', 'Function')
    cases_df.columns = cases_df.columns.str.replace('date_created', 'Date')
    cases_df.columns = cases_df.columns.str.replace('time', 'Time')
    cases_df.columns = cases_df.columns.str.replace('id', 'ID')
  

    behavior = pd.get_dummies(cases_df['Behavior'])
    anticedent = pd.get_dummies(cases_df['Antecedent'])
    consequence = pd.get_dummies(cases_df['Consequence'])
    function = pd.get_dummies(cases_df['Function'])
    df_matrix = pd.concat([cases_df,behavior, anticedent, consequence, function], axis=1)
    df_matrix.drop(['Behavior','Antecedent','Function', 'Consequence','Date','Time','ID'],axis=1,inplace=True)
    matrix = df_matrix.corr().round(2) 

    context = {
        'student':student,
        'unique_abcf_count':unique_abcf_count.to_html(index=False),
        'unique_abc_count':unique_abc_count.to_html(index=False),
        'unique_abf_count':unique_abf_count.to_html(index=False),
        'unique_bf_count':unique_bf_count.to_html(index=False),
        'duplicateRows':duplicateRows.to_html(index=False),
        'unique_ab_count':unique_ab_count.to_html(index=False),
    
        'unique_bs_count':unique_bs_count.to_html(index=False),
        
        # 'unique_hour':unique_hour.to_html(),

       'unique_hour_html':unique_hour_html,

        'unique_b_count':unique_b_count.to_html(index=False),
         
    
        'duration_html':duration_html,
        #  'duration_behavior':duration_behavior.to_html(index=False),
        
        'frequency_behavior':frequency_behavior.to_html(index=False),
        'matrix':matrix.to_html(),
        'intensity_html':intensity_html,

        }

    return render(request, 'bip/raw_data.html', context)


# download the raw_data.html as a word dument and write the function xxxxxxxx


# Create an HTML file for the upload form

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

def assign_data_entry(request, pk):
  
    student = get_object_or_404(Student, pk=pk)
    student_behaviors = student.case_set.all() 
    behavior = Behavior.objects.all()
    casemanager = models.CaseManager.objects.all()
    case = Case.objects.all()
    studentcurrent = Student.objects.get(id=pk)

    context = {
    'student_behaviors':student_behaviors,
    "student":student,
    'case':case,
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


def export(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_behaviors = student.case_set.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FBA Data.csv"'
    writer = csv.writer(response)

    headers = ["User","Case", "Behavior", "Frequency","Antecedent", "Consequence", "Function","Date"]
    
    has_setting = student_behaviors.filter(enviroment__isnull=False).exists()

    has_intensity = student_behaviors.filter(intensity__isnull=False).exists()


    has_duration = student_behaviors.filter(duration__isnull=False).exists()
    # has_frequency = student_behaviors.filter(frequency__isnull=False).exists()
    # has_date = student_behaviors.filter(date_created__isnull=False).exists()

    has_time = student_behaviors.filter(time__isnull=False).exists()


    if has_setting:
        headers.append("Setting")

    if has_intensity:
        headers.append("Intensity")
   
    
    if has_duration:
        headers.append("Duration(Sec)")

    if has_time:
        headers.append("Time")


      

    writer.writerow(headers)

    for case in student_behaviors:
        setting_value = case.enviroment if case.enviroment is not None else ''

        # date_value = case.date_created.strftime("%Y-%m-%d")


        time_value = case.time if case.time is not None else ''
        duration_value = case.duration if case.duration is not None else ''


        intensity_value = case.intensity if case.intensity is not None else ''



        # frequency_value = case.frequency if case.frequency is not None else ''

        # date_value = case.date_created if case.date_created.strftime("%Y-%m-%d") is not None else ''


        row = [
            case.user.username,
            case.student.studentname,
            case.behavior.behaviorincident,
            case.frequency,
            case.anticedent.anticedentincident,
            case.consequence.behaviorconsequence,
            case.function.behaviorfunction,
            case.date_created,


        ]

        if has_setting:
            row.append(setting_value)

        if has_intensity:
            row.append(intensity_value)

        if has_duration:
            row.append(duration_value)


        if has_time:
            row.append(time_value)

        
        writer.writerow(row)

    return response


def upload_page(request,pk):


    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 

    context = {'student':student}

    return render(request, 'bip/upload_page.html', context) 

def upload_options(request,pk):
    student = get_object_or_404(Student, pk=pk)
    student_cases = student.case_set.all() 
    
    
    context = {

        'student':student
    }
    return render(request, 'bip/upload_options.html', context) 


# this works so far I think
def case_upload_csv(request):
    template = "bip/upload.html"
    prompt = {'order': 'Order of the CSV should be case, behavior, anticedent, consequence, function, environment'}

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        student_name = column[1]
        behavior_name = column[2]
        frequency_value = column[3]
        anticedent_name = column[4]
        consequence_name = column[5]
        function_name = column[6]
        date_created = column[7] 
        enviroment_name = column[8] if len(column) > 8 else None


        
        user_instance, _ = User.objects.get_or_create(username=username)
        student_instance, _ = Student.objects.get_or_create(
            studentname=student_name,
            user_student=user_instance
        )

        behavior_instance, _ = Behavior.objects.get_or_create(
            behaviorincident=behavior_name,
            student=student_instance,
            user=user_instance
        )
        anticedent_instance, _ = Anticedent.objects.get_or_create(
            anticedentincident=anticedent_name,
            student=student_instance,
            user=user_instance
        )
        consequence_instance, _ = Consequence.objects.get_or_create(
            behaviorconsequence=consequence_name,
            student=student_instance,
            user=user_instance
        )
        function_instance, _ = Function.objects.get_or_create(
            behaviorfunction=function_name,
            student=student_instance,
            user=user_instance
        )

        if enviroment_name:
             enviroment_instance, _ = Enviroment.objects.get_or_create(
                 behaviorenviroment=enviroment_name,
                 student=student_instance,
                 user=user_instance
            )
        else:
            enviroment_instance = None 

        
        try:
            Case.objects.create(
                behavior=behavior_instance,
                frequency=frequency_value, # Assign the extracted frequency value
                anticedent=anticedent_instance,
                consequence=consequence_instance,
                function=function_instance,
                date_created=date_created,
                student=student_instance,
                enviroment=enviroment_instance,

                user=user_instance,

                # Add other fields from your model accordingly
            )
        except IntegrityError:
            # Handle IntegrityError (log, pass, or customize as needed)
            pass

    context = {}
    return render(request, "bip/welcome_user.html", context)



    # This adds Duration


def case_upload_csv_duration(request):
    template = "bip/upload_duration.html"
    prompt = {'order': 'Order of the CSV should be case, behavior, anticedent, consequence, function, duration, environment'}

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        student_name = column[1]
        behavior_name = column[2]
        frequency_value = column[3]
        anticedent_name = column[4]
        consequence_name = column[5]
        function_name = column[6]
        date_created = column[7] 
        duration_value = column[8]  # Extract the duration value from the CSV
        enviroment_name = column[9] if len(column) > 9 else None



        
        user_instance, _ = User.objects.get_or_create(username=username)
        student_instance, _ = Student.objects.get_or_create(
            studentname=student_name,
            user_student=user_instance
        )

        behavior_instance, _ = Behavior.objects.get_or_create(
            behaviorincident=behavior_name,
            student=student_instance,
            user=user_instance
        )
        anticedent_instance, _ = Anticedent.objects.get_or_create(
            anticedentincident=anticedent_name,
            student=student_instance,
            user=user_instance
        )
        consequence_instance, _ = Consequence.objects.get_or_create(
            behaviorconsequence=consequence_name,
            student=student_instance,
            user=user_instance
        )
        function_instance, _ = Function.objects.get_or_create(
            behaviorfunction=function_name,
            student=student_instance,
            user=user_instance
        )

        if enviroment_name:
             enviroment_instance, _ = Enviroment.objects.get_or_create(
                 behaviorenviroment=enviroment_name,
                 student=student_instance,
                 user=user_instance
            )
        else:
            enviroment_instance = None 
      
        try:
            Case.objects.create(
                behavior=behavior_instance,
                frequency=frequency_value, # Assign the extracted frequency value
                anticedent=anticedent_instance,
                consequence=consequence_instance,
                function=function_instance,
                date_created=date_created,
                student=student_instance,
                duration=duration_value,  # Assign the extracted duration value
                enviroment=enviroment_instance,



                user=user_instance,

                # Add other fields from your model accordingly
            )
        except IntegrityError:
            # Handle IntegrityError (log, pass, or customize as needed)
            pass

    context = {}
    return render(request, "bip/welcome_user.html", context)

    

    # This is the time upload:




def case_upload_csv_time(request):
    template = "bip/upload_time.html"
    prompt = {'order': 'Order of the CSV should be case, behavior, anticedent, consequence, function, duration, environment'}
    
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        student_name = column[1]
        behavior_name = column[2]
        frequency_value = column[3]
        anticedent_name = column[4]
        consequence_name = column[5]
        function_name = column[6]
        date_created = column[7] 

        time_value = column[8]

        enviroment_name = column[9] if len(column) > 9 else None



        
        user_instance, _ = User.objects.get_or_create(username=username)
        student_instance, _ = Student.objects.get_or_create(
            studentname=student_name,
            user_student=user_instance
        )

        behavior_instance, _ = Behavior.objects.get_or_create(
            behaviorincident=behavior_name,
            student=student_instance,
            user=user_instance
        )
        anticedent_instance, _ = Anticedent.objects.get_or_create(
            anticedentincident=anticedent_name,
            student=student_instance,
            user=user_instance
        )
        consequence_instance, _ = Consequence.objects.get_or_create(
            behaviorconsequence=consequence_name,
            student=student_instance,
            user=user_instance
        )
        function_instance, _ = Function.objects.get_or_create(
            behaviorfunction=function_name,
            student=student_instance,
            user=user_instance
        )

        if enviroment_name:
             enviroment_instance, _ = Enviroment.objects.get_or_create(
                 behaviorenviroment=enviroment_name,
                 student=student_instance,
                 user=user_instance
            )
        else:
            enviroment_instance = None 
      
        try:
            Case.objects.create(
                behavior=behavior_instance,
                frequency=frequency_value, # Assign the extracted frequency value
                anticedent=anticedent_instance,
                consequence=consequence_instance,
                function=function_instance,
                date_created=date_created,
                student=student_instance,
                time=time_value,  # Add the time here
                enviroment=enviroment_instance,



                user=user_instance,

                # Add other fields from your model accordingly
            )
        except IntegrityError:
            # Handle IntegrityError (log, pass, or customize as needed)
            pass

    context = {}
    return render(request, "bip/welcome_user.html", context)




    # upload get_multiple_line_plot_chatgpt


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%y').date()
    except ValueError:
        return None

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return None

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False




def case_upload_csv_multiple(request):
    template = "bip/upload_multiple.html"


    
    prompt = {
        'order': ', Multiple'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES.get('file')
    if not csv_file or not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')
        return render(request, template, prompt)

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)  # Skip the header row

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        # Extend the column list to avoid IndexError
        column = (column + [None] * 11)[:11]
        user_username, student_name, behavior_name, frequency_str, antecedent_name, consequence_name, function_name, date_str, duration_str, time_str, setting_name = column

        # Fetch or create related instances
        user_instance, _ = User.objects.get_or_create(username=user_username)
        student_instance, _ = Student.objects.get_or_create(
            studentname=student_name,
            defaults={'user_student': user_instance}
        )
        behavior_instance = Behavior.objects.filter(
        behaviorincident=behavior_name,
        student=student_instance,
        user=user_instance
        ).first()

        if not behavior_instance:
            behavior_instance = Behavior.objects.create(
                behaviorincident=behavior_name,
                student=student_instance,
             user=user_instance
        )
        anticedent_instance, _ = Anticedent.objects.get_or_create(
            anticedentincident=antecedent_name,
            defaults={'student': student_instance, 'user': user_instance}
        )
        consequence_instance, _ = Consequence.objects.get_or_create(
            behaviorconsequence=consequence_name,
            defaults={'student': student_instance, 'user': user_instance}
        )
        function_instance, _ = Function.objects.get_or_create(
            behaviorfunction=function_name,
            defaults={'student': student_instance, 'user': user_instance}
        )
        enviroment_instance = None
        if setting_name:
            enviroment_instance, _ = Enviroment.objects.get_or_create(
                behaviorenviroment=setting_name,
                defaults={'student': student_instance, 'user': user_instance}
            )

        # Parse optional date and time fields
        date_created = parse_date(date_str) if date_str else timezone.now().date()
        time_created = parse_time(time_str) if time_str else None
        duration = int(duration_str) if duration_str and is_integer(duration_str) else None
        frequency = int(frequency_str) if frequency_str and is_integer(frequency_str) else 1

        # Create the Case instance
        try:
            Case.objects.create(
                student=student_instance,
                behavior=behavior_instance,
                user=user_instance,
                anticedent=anticedent_instance,
                consequence=consequence_instance,
                function=function_instance,
                date_created=date_created,
                duration=duration,
                time=time_created,
                frequency=frequency,
                enviroment=enviroment_instance
            )
        except IntegrityError as e:
            messages.error(request, f'An error occurred while creating a case: {e}')

    return render(request, "bip/welcome_user.html", {})

