import os
import random
import string
from importlib import import_module

from six import string_types

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
