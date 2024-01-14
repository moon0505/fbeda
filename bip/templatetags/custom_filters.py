from django import template



register = template.Library()

@register.filter(name='is_case_manager')
def is_case_manager(user):
    return user.groups.filter(name='CASE MANAGER').exists()




@register.filter(name='is_data_entry')
def is_data_entry(user):
    return user.groups.filter(name='DATA ENTRY').exists()