# utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = 'Your OTP for Fruitkha Registration'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)
