import os
import random
import string
from importlib import import_module

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from six import string_types

from env import EMAIL_API_KEY, EMAIL_ID

def send_mail(to,subject,body):
    email_id = to
    message = Mail(
        from_email=EMAIL_ID,
        to_emails = email_id,
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(EMAIL_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception as e:
        print(e) 
        return False

def randomKey(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def unique_random_key(instance):
    new_key= randomKey()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(joining_key= new_key).exists()
    if qs_exists:
        return randomKey(instance)
    return new_key


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)
