from django.db.models.signals import pre_save

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import CustomUser
from .models import CaseManager





@receiver(post_save, sender=CustomUser)
def notify_superusers_on_new_user(sender, instance, created, **kwargs):
    if created:
        superusers_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        subject = 'New User Registered'
        message = f'A new user has registered: {instance.username} (email: {instance.email})'
        from_email = 'noreply@exploratoryfba.com'  # Use an appropriate sender email
        send_mail(subject, message, from_email, superusers_emails, fail_silently=False)



@receiver(pre_save, sender=CaseManager)
def send_status_active_email(sender, instance, **kwargs):
    # Attempt to fetch the instance from the database to compare statuses
    if instance.pk:
        old_instance = CaseManager.objects.filter(pk=instance.pk).first()
        if old_instance and not old_instance.status and instance.status:
            # The status changed from False to True
            send_mail(
                'Your EFBA Account is Active',
                f'Hello, you can now login to your account. \nThank you for using EFBA!',
                'exploratoryfba.com',
                [instance.user.email],
                fail_silently=False,
            )
