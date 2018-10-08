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
    def create_listing(self, form_data, user_id):
        # empty errors list
        errors = []

        # Address
        # ...address
        if len(form_data['addressLine1']) == 0:
            errors.append('Address can not be left empty!')
        # ...city
        if len(form_data['city']) == 0:
            errors.append('City can not be left empty!')
        # state
        if len(form_data['state']) == 0:
            errors.append('State can not be left empty!')
        if len(form_data['state']) > 2:
            errors.append('Enter the abbreviation of the state only!')
        # ...check state is valid or not
        list_of_state = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
        
        found = False
        for list in list_of_state:
            if form_data['state'] == list:
                found = True
                break
        
        if found:
            print form_data['state']
        else:
            errors.append('Invalid state!')

        # zip code
        if len(form_data['zip']) == 0:
            errors.append('Zipcode can not be left empty!')
        if len(form_data['zip']) > 6:
            errors.append('Invalid zipcode!')
        
        # Details
        # ...price
        if len(form_data['price']) == 0:
            errors.append('Price can not be left empty!')
        # # ...bedrooms
        # if type(form_data['bedrooms']) != int:
        #     errors.append('Bedroooms must be numbers only!')
        # # ...bathrooms
        # if type(form_data['bathrooms']) != float or type(form_data['bathrooms']) != int:
        #     errors.append('Bathrooms must be numbers only!')
        # # ...sq foot
        # if type(form_data['sqFootage']) != int:
        #     errors.append('Square footage must be numbers only!')
        # # ...lot size
        # if type(form_data['lotSize']) != int:
        #     errors.append('Lot size must be numbers only!')
        
        # check if any errors
        if errors: # if true, display errors
            return (False, errors)

        # store listing to database
        create_listing = self.create(addressOne=form_data['addressLine1'],addressTwo=form_data['addressLine2'],city=form_data['city'],state=form_data['state'],zipcode=form_data['zip'],price=form_data['price'],listing_type=form_data['listing-type'],bedrooms=form_data['bedrooms'],bathrooms=form_data['bathrooms'],sq_footage=form_data['sqFootage'],lot_size=form_data['lotSize'],desc=form_data['desc'],agentId=User.objects.get(id=user_id),image=form_data['thumbnail'])
        
        print 'ADDED LISTING SUCCESSFULLY! This is the address: {}'.format(create_listing)

        return (True, create_listing.id)


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
    price = models.CharField(max_length=255)
    listing_type = models.CharField(max_length=1, choices=LISTING_TYPE_CHOICES)
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    sq_footage = models.IntegerField()
    lot_size = models.IntegerField()
    desc = models.TextField()
    agentId = models.ForeignKey(User, related_name="agent_id")
    
    # Image
    image = models.ImageField(upload_to='./static/images/')

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