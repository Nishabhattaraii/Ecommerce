
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(email, reset_link):
    subject = "Password Reset Request"
    message = f"Click the link to reset your password: {reset_link}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def send_password_change_confirmation_email(email):
    subject = "Password Changed Successfully"
    message = "Your password has been successfully changed. If you did not make this change, please contact support immediately."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
