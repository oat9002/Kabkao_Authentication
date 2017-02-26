from django.contrib.auth.models import User
from django.db import models

class UserProxy(User):

    class Meta:
        proxy = True
        permissions = (
            ('view_user', 'View user'),
        )