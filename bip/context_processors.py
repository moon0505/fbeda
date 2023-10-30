
from django.contrib.auth import get_user

def user_context(request):
    user = get_user(request)
    return {'user': user}
