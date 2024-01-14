from django import template



register = template.Library()

@register.filter(name='is_case_manager')
def is_case_manager(user):
    return user.groups.filter(name='CASE MANAGER').exists()