
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import CustomUser

@receiver(post_save, sender=CustomUser)
def notify_superusers_on_new_user(sender, instance, created, **kwargs):
    if created:
        superusers_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        subject = 'New User Registered'
        message = f'A new user has registered: {instance.username} (email: {instance.email})'
        from_email = 'noreply@exploratoryfba.com'  # Use an appropriate sender email
        send_mail(subject, message, from_email, superusers_emails, fail_silently=False)
