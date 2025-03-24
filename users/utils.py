import uuid
from django.core.mail import send_mail

def generateToken():
    token = uuid.uuid4()
    return token


def sendVerificationEmail(user, token, request):
    subject = 'Verify your email address'
    link = f'http://{request.META['HTTP_HOST']}/api/users/verify-email/?token={token}'
    message = f'Click the following link to verify your email address: {link}'
    from_email = 'gabrielgomezrojas0501@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)