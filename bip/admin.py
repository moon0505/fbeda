





from django.contrib import admin
from bip.models import  Student, Behavior,Case,Anticedent,Function,Consequence
from bip.models import CaseManager,DataEntry
from bip.forms import CaseManagerUserForm, DataEntryUserForm




class CaseMangerAdmin(admin.ModelAdmin):
    pass
admin.site.register(CaseManager, CaseMangerAdmin)

class DataEntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataEntry, DataEntryAdmin)




admin.site.register(Behavior)
admin.site.register(Case)
admin.site.register(Student)
admin.site.register(Anticedent)
admin.site.register(Function)
admin.site.register(Consequence)





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




