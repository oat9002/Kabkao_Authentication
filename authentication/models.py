from django.contrib.auth.models import User
from django.db import models

class UserProxy(User):

    class Meta:
        proxy = True
        permissions = (
            ('view_user', 'View user'),
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()


class CustomPermission(models.Model):

    class Meta:
        managed = False
        permissions = (
            ('add_menu', 'Can add menu'),
            ('view_menu', 'Can view menu'),
            ('change_menu', 'Can change menu'),
            ('delete_menu', 'Can delete menu'),
            ('add_order', 'Can add order'),
            ('view_order', 'Can view order'),
            ('change_order', 'Can change order'),
            ('delete_order', 'Can delete order'),
        )