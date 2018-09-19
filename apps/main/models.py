from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
# USER
# user manager
class UserManager(models.Manager):
    pass

# user table
class User(models.Model):
    PERMISSION_LEVEL_CHOICES = (
        ('U', 'USER'),
        ('G', 'AGENT'),
        ('A', 'ADMINISTRATOR')
    )

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)                                 
    permissionLevel = models.CharField(max_length=1, choices=PERMISSION_LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)

# LISTING
# user manager
# user table

# IMAGE
# user manager
# user table