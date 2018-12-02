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

# CONTACT US
# contact ticket manager
class ContactTicketManager(models.Manager):
    # validate ticket
    def validateTicket(self,form_data,contactType):
        # empty errors list
        errors = []

        # Validate Name
        # ... check if null or atleast 2 character
        if len(form_data['name']) < 2:
            errors.append('Name must be at least 2 characters')

        # Validate email
        # ... email format
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Email entered is not valid')

        # Validate phone
        # ... check length of phone
        if len(form_data['phone']) == 0:
            errors.append('Phone must be entered!')
        
        # Validate message
        # ... check length of message
        if len(form_data['message']) == 0:
            errors.append('Message must be entered!')

        # check if any errors
        if errors: # if true, display errors
            return (False, errors)

        # store user to database
        add_ticket = self.create(name=form_data['name'],email=form_data['email'],phone=form_data['phone'],message=form_data['message'],contact_type=contactType)
        print 'ADDED TICKET SUCCESSFULLY! This is the ticket: {}'.format(add_ticket)

        return (True, add_ticket.id)

# contact ticket table
class ContactTicket(models.Model):
    CONTACT_TYPE_CHOICES = (
        ('A', 'ADMIN'),
        ('G', 'AGENT'),
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)                                 
    message = models.TextField()
    contact_type = models.CharField(max_length=1, choices=CONTACT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    # call user manager
    objects = ContactTicketManager()

    # print user created
    def __str__(self):
        return self.email

# LISTING
# listing manager
class ListingManager(models.Manager):
    def create_listing(self, form_data, user_id, image_path):
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
        
        format_price = (form_data['price']).split(',')

        if len(form_data) > 1:
            price = "".join(format_price)
        else:
            price = form_data['price']

        # ...bedrooms
        if len(form_data['bedrooms']) == 0:
            errors.append('Bedroooms can not be left empty!')
        # ...bathrooms
        if len(form_data['bathrooms']) == 0:
            errors.append('Bathrooms can not be left empty!')
        # ...sq foot
        if len(form_data['sqFootage']) == 0:
            errors.append('Square footage can not be left empty!')
        # ...lot size
        if len(form_data['lotSize']) == 0:
            errors.append('Lot size can not be left empty!')
        # ...image
        if image_path == 'no image uploaded':
            errors.append('Must upload image!')
        
        # check if any errors
        if errors: # if true, display errors
            return (False, errors)

        # store listing to database
        create_listing = self.create(addressOne=form_data['addressLine1'],addressTwo=form_data['addressLine2'],city=form_data['city'],state=form_data['state'],zipcode=form_data['zip'],price=price,listing=form_data['listing-type'],bedrooms=form_data['bedrooms'],bathrooms=form_data['bathrooms'],sq_footage=form_data['sqFootage'],lot_size=form_data['lotSize'],desc=form_data['desc'],agentId=User.objects.get(id=user_id),image=image_path)

        print 'ADDED LISTING SUCCESSFULLY! This is the address: {}'.format(create_listing)

        return (True, create_listing.id)

    def edit_listing(self, form_data,listing_id, user_id, image_path):
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

        format_price = (form_data['price']).split(',')

        try_price = ("".join(format_price)).split('.')
        price = try_price[0]

        # new_price = format_price.split('.')
        print (''.join(format_price)).split('.')
        
        # ...bedrooms
        if len(form_data['bedrooms']) == 0:
            errors.append('Bedroooms can not be left empty!')
        # ...bathrooms
        if len(form_data['bathrooms']) == 0:
            errors.append('Bathrooms can not be left empty!')
        # ...sq foot
        if len(form_data['sqFootage']) == 0:
            errors.append('Square footage can not be left empty!')
        # ...lot size
        if len(form_data['lotSize']) == 0:
            errors.append('Lot size can not be left empty!')
        
        # check if any errors
        if errors: # if true, display errors
            return (False, errors)

        # store listing to database
        edit_listing = self.filter(id=listing_id,agentId=user_id).update(addressOne=form_data['addressLine1'],addressTwo=form_data['addressLine2'],city=form_data['city'],state=form_data['state'],zipcode=form_data['zip'],price=price,listing=form_data['listing-type'],bedrooms=form_data['bedrooms'],bathrooms=form_data['bathrooms'],sq_footage=form_data['sqFootage'],lot_size=form_data['lotSize'],desc=form_data['desc'],agentId=User.objects.get(id=user_id),image=image_path)

        print 'EDITED LISTING SUCCESSFULLY! This is the listing id: {}!'.format(listing_id)

        return (True, edit_listing)


# listing table
class Listing(models.Model):
    LISTING_CHOICES = (
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
    zipcode = models.CharField(max_length=255)
    
    # Details
    price = models.IntegerField()
    listing = models.CharField(max_length=1, choices=LISTING_CHOICES)
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    sq_footage = models.IntegerField()
    lot_size = models.FloatField()
    desc = models.TextField()
    agentId = models.ForeignKey(User, related_name="agent_id")
    
    # Image
    image = models.FilePathField(path='media/')

    # timestaps
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ListingManager()

    def __str__(self):
        return self.addressOne