from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# EMAIL Regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
# USER
# user manager
class UserManager(models.Manager):
    # validate login
    def validateLogin(self,form_data):
        # empty errors list
        errors = []
        
        # check wether user exists or not
        try:
            # check for if user exists
            check_user = self.get(email=form_data['email'])
            print 'User logged in with : {} & Matched with this many emails : {}'.format(form_data['email'],check_user)
            # if user exists
            # ... check password
            if not bcrypt.checkpw(form_data['password'].encode(), check_user.password.encode()):
                errors.append('Email/Password is invalid')
                return (False, errors)
            # If password valid
            # ... login in user
            return (True, check_user.id)
        except:
            # if user not found
            errors.append('Email/Password is invalid')

            return (False, errors)

    # validate registeration
    def validateRegister(self,form_data):
        # empty errors list
        errors = []

        # Validate Name
        # ... check if null or atleast 2 character
        if len(form_data['firstName']) < 2:
            errors.append('First name must be at least 2 characters')
        if len(form_data['lastName']) < 2:
            errors.append('Last name must be at least 2 characters')

        # Validate email
        # ... email format
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Email entered is not valid')

        # Validate password
        # ... check length of password
        if len(form_data['password']) < 8:
            errors.append('Password must be atleast 8 characters long')
        # ... check if password matchs confrim password
        elif form_data['password'] != form_data['confirmPassword']:
            errors.append('Passwords must match')

        # check if any errors
        if errors: # if true, display errors
            return (False, errors)

        # check if user exists
        try:
            check_user = self.get(email=form_data['email'])
            errors.append('User already exists')
            return (False, errors)
        # if user does not exist
        except:
            # ... hash password
            pwd = form_data['password']
            hash_pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

            # store user to database
            add_user = self.create(firstName=form_data['firstName'],lastName=form_data['lastName'],email=form_data['email'],password=hash_pwd,permissionLevel='U')
            print 'ADDED USER SUCCESSFULLY! This is the user: {}'.format(add_user)

        return (True, add_user.id)

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
    updated_at = models.DateTimeField(auto_now=True)

    # call user manager
    objects = UserManager()

    # print user created
    def __str__(self):
        return self.email

# LISTING
# listing manager
class ListingManager(models.Manager):
    pass

# listing table
class Listing(models.Model):
    LISTING_TYPE_CHOICES = (
        ('S', 'Single-Family Home'),
        ('A', 'Apartment'),
        ('C', 'Condo'),
        ('T', 'Townhouse'),
        ('L', 'Land'),
        ('M', 'Mult-Family Home'),
        ('F', 'Farm/Ranch')
    )

    # Address
    addressOne = models.CharField(max_length=255)
    addressTwo = models.CharField(max_length=255)  
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255) 
    zipcode = models.IntegerField()
    
    # Details
    price = models.IntegerField()
    listing_type = models.CharField(max_length=1, choices=LISTING_TYPE_CHOICES)
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    sq_footage = models.IntegerField()
    lot_size = models.IntegerField()
    desc = models.TextField()
    agentId = models.ForeignKey(User, related_name="agent_id")
    
    # Image
    image = models.ImageField(upload_to='houses')

    # timestaps
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ListingManager()

    def __str__(self):
        return self.addressOne

# IMAGE
# image manager

# image table
# class Images(models.Model):
#     fileName = models.CharField(max_length=255)
#     path = models.CharField(max_length=255)
#     active = models.IntegerField()
#     listingId = models.ForeignKey(Listing, related_name="listing_id")