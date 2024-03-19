

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from bip import views



app_name = 'bip'


urlpatterns = [

    # case manager and data entry urls for login and access-----------------
    



    
    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('case_manager_signup/', views.case_manager_signup_view,name='case_manager_signup'),
    
    path('case_manager_login/', LoginView.as_view(template_name='account/case_manager_login.html'),name='case_manager_login'),

    
    path('data_entry_signup/', views.data_entry_signup_view, name='data_entry_signup'),
    path('data_entry_login/', LoginView.as_view(template_name='account/data_entry_login.html'), name='data_entry_login'),
    

    path('data_entry_dashboard', views.data_entry_dashboard_view,name='data_entry_dashboard'),

    path('casemanagerclick', views.casemangerclick_view),
    path('dataentryclick', views.dataentryclick_view),

    path('data_entry_input/<pk>/', views.data_entry_input_view, name='data_entry_input'),

    path('case_manager_dashboard/<int:pk>', views.case_manager_dashboard_view,name='case_manager_dashboard'),

    path('admin_data_entry_approve/<int:pk>', views.admin_approve_data_entry_view,name='admin_data_entry_approve'),
    
    path('approved_data_entry/<int:pk>', views.approved_data_entry_view,name='approved_data_entry'),
    
    path('admin_delete_data_entry/<int:pk>', views.admin_delete_data_entry_view,name='admin_delete_data_entry'),
    
    path('delete_data_entry/<int:pk>', views.delete_data_entry_view,name='delete_data_entry'),

    path('reject_data_entry/<int:pk>', views.reject_data_entry_view,name='reject_data_entry'),
    
   
    path('assign_data_entry/<pk>/', views.assign_data_entry, name='assign_data_entry'),
    
    path('updateunique_case_identifier/<pk>/', views.updateunique_case_identifier, name='updateunique_case_identifier'),
    

    path('case_manager_unique_identifier/<pk>/', views.case_manager_unique_identifier, name='case_manager_unique_identifier'),
    



    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= 'account/password_reset.html'), 
         name='reset_password'),

   
   

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
          name='password_reset_done'),


    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),

    
    # the core of the website--------------------------------
    
    path('home/', views.HomePage.as_view(), name="home"),


    path('luna/', views.luna, name="luna"),
    path('additional_notes/', views.additional_notes_view, name="additional_notes"),

    
    path('statistics/<pk>/', views.statistics, name="statistics"),

    path('', views.description_view, name="description"),

    
    path('student_list/<pk>/', views.list_view, name='student_list'),

    path("by/<username>/",views.UserPosts.as_view(),name="for_user"),
    
    path('dashboard/<pk>/', views.dashboard, name='dashboard'),
    
    path('create_incident/<pk>/', views.behavior_form_view, name='create_incident'),
    
    path('updatepost/<int:pk>/<int:student_id>/', views.updatePost, name='updatepost'),

    path("by/<username>/",views.UserPosts.as_view(),name="for_user"),

    path('delete_post/<pk>/', views.deletePost, name='delete_post'),
        
    path('create_student/', views.create_student, name='create_student'),
    
    
    path('update_student/<pk>/',views.updateStudent,name='update_student'),
    
    
    path('delete_student/<pk>/',views.deleteStudent,name='delete_student'),
     
    path('delete_user/<pk>/',views.deleteUser,name='delete_user'),

    path('user_account/<pk>/',views.user_account,name='user_account'),


    path('create_unique_id/<pk>/',views.create_unique_id,name='create_unique_id'),

    path('case_profile/<pk>/',views.student_profile,name='student_profile'),

    
    path('create_behavior/<pk>/', views.create_behavior, name='create_behavior'),
    path('update_behavior/<pk>/',views.updateBehavior,name='update_behavior'),
    path('delete_behavior/<pk>/', views.deleteBehavior, name='delete_behavior'),
    

    path('edit_behavior/<pk>/', views.edit_behavior_view, name='edit_behavior'),
    path('edit_anticedent/<pk>/', views.edit_anticedent_view, name='edit_anticedent'),
    path('edit_consequence/<pk>/', views.edit_consequence_view, name='edit_consequence'),
    path('edit_function/<pk>/', views.edit_function_view, name='edit_function'),


    path('create_anticedent/<pk>/', views.create_anticedent, name='create_anticedent'),
    path('update_anticedent/<pk>/',views.updateAnticedent,name='update_anticedent'),
    path('delete_anticedent/<pk>/', views.deleteAnticedent, name='delete_anticedent'),
    
    
    path('create_function/<pk>/', views.create_function, name='create_function'),
    
    path('update_function/<pk>/',views.updatFunction,name='update_function'),
    
    path('delete_function/<pk>/', views.deleteFunction, name='delete_function'),
    
    
    
    
    path('create_consequence/<pk>/', views.create_consequence, name='create_consequence'),
     
    path('update_consequence/<pk>/',views.updateConsequence,name='update_consequence'),
    path('delete_consequence/<pk>/', views.deleteConsequence, name='delete_consequence'),
    
    path('create_setting/<pk>/', views.create_setting_view, name='create_setting'),
    path('update_setting/<pk>/',views.updateSetting,name='update_setting'),
    path('edit_setting/<pk>/', views.edit_enviroment_view, name='edit_setting'),
    path('delete_setting/<pk>/', views.deleteEnviroment, name='delete_setting'),

    path('error_page/<pk>/', views.error_page, name='error_page'),

    path('correlation/<pk>/', views.correlation_view, name='correlation'),
    path('pie_charts/<pk>/', views.pie_chart_view, name='pie_charts'),


    path('snapshot/<pk>/', views.snapshot_view, name='snapshot'),
    path('snapshot_data_entry/<pk>/', views.snapshot_data_entry_view, name='snapshot_data_entry'),

    
    path('function/<pk>/', views.function_view, name='function'),
    path('consequence/<pk>/', views.consequence_view, name='consequence'),


    path('machine_learning/<pk>/', views.train_naive_bayes, name='machine_learning'),

    path('download_chart_pdf/<pk>/', views.download_chart_pdf, name='download_chart_pdf'),

    path('download_antecedent_chart_pdf/<pk>/', views.download_antecedent_chart_pdf, name='download_antecedent_chart_pdf'),

    path('download_consequence_chart_pdf/<pk>/', views.download_consequence_chart_pdf, name='download_consequence_chart_pdf'),
    
    
    
    path('download_function_chart_pdf/<pk>/', views.download_function_chart_pdf, name='download_function_chart_pdf'),

    path('anticedent/<pk>/', views.anticedent_view, name='anticedent'),

    path('setting/<pk>/', views.enviroment_view, name='setting'),

    
    
    path('filter_data/<pk>/', views.filter_data, name='filter_data'),
    
    
    
    path('chart/<pk>/', views.chart_view, name='chart'),



    path('raw_data/<pk>/', views.raw_data, name='raw_data'),

    path('export/<pk>/', views.export, name='export'),


    path('upload_page/<pk>/', views.upload_page, name='upload_page'),
    path('case_upload_csv/', views.case_upload_csv, name='case_upload_csv'),  
    path('upload_options/<pk>/', views.upload_options, name='upload_options'),
    path('case_upload_csv_duration/', views.case_upload_csv_duration, name='case_upload_csv_duration'),  
    path('case_upload_csv_time/', views.case_upload_csv_time, name='case_upload_csv_time'),  
    path('case_upload_csv_multiple/', views.case_upload_csv_multiple, name='case_upload_csv_multiple'),  


    
    path('download_page/', views.download_page, name='download_page'),

    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout/", views.user_logout, name="logout"),


  
    path('video/', views.show_video, name='show_video'),

    # artificial inttelligence urls--------------------------------
    path('function_ai_abc/<pk>/', views.function_ai_abc, name='function_ai_abc'),
    path('antecedent_ai/<pk>/', views.antecedent_ai, name='antecedent_ai'),
    path('intervention_ai_abc/<pk>/', views.intervention_ai_abc, name='intervention_ai_abc'),
,




]

