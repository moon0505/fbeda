

from django.contrib import admin
from bip.models import Student, Behavior, Case, Anticedent, Function, Consequence, Enviroment
from bip.models import CaseManager, DataEntry
from bip.forms import CaseManagerUserForm, DataEntryUserForm

from django.contrib.auth.admin import UserAdmin  # Import the UserAdmin from django.contrib.auth.admin
from .models import CustomUser 


class CustomUserAdmin(UserAdmin):
    # Define the fields you want to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'last_login','is_staff')

class CaseMangerAdmin(admin.ModelAdmin):
    pass

class DataEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CaseManager, CaseMangerAdmin)
admin.site.register(DataEntry, DataEntryAdmin)
# Register other models
admin.site.register(Behavior)
admin.site.register(Case)
admin.site.register(Student)
admin.site.register(Anticedent)
admin.site.register(Function)
admin.site.register(Consequence)
admin.site.register(Enviroment)



# from django.contrib import admin
# from bip.models import  Student, Behavior,Case,Anticedent,Function,Consequence,Enviroment
# from bip.models import CaseManager,DataEntry
# from bip.forms import CaseManagerUserForm, DataEntryUserForm




# class CaseMangerAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(CaseManager, CaseMangerAdmin)

# class DataEntryAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(DataEntry, DataEntryAdmin)




# admin.site.register(Behavior)
# admin.site.register(Case)
# admin.site.register(Student)
# admin.site.register(Anticedent)
# admin.site.register(Function)
# admin.site.register(Consequence)
# admin.site.register(Enviroment)





# class MyUserAdmin(UserAdmin):
#     add_form = MyUserCreationForm
#     form = MyUserChangeForm
    
#     model = MyUser
    
#     list_display = ['username', 'occupation', 'institution','email']
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('occupation', 'institution')}),
#     ) #this will allow to change these fields in admin module

# admin.site.register(MyUser, MyUserAdmin)

# class CaseMangerAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(CaseManager, CaseMangerAdmin)

# class DataEntryAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(DataEntry, DataEntryAdmin)


# # admin.site.register(Behavior)
# # admin.site.register(Case)
# admin.site.register(Student)




# Register your models here.




