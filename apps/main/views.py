from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.

# Render Templates

# home - /
def home(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
    
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
        print user
    else:
        user = ''

    # LISTINGS
    # ...recently added
    # ...featured home
    # ...most affordable homes

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user
    }

    return render(request,'index.html',context)

# login - /login
def login(request):
    # check if user in session
    if 'user_id' in request.session:
        return redirect('main:dashboard')

    return render(request,'login.html')

# registration - /register
def register(request):
    # check if user in session
    if 'user_id' in request.session:
        return redirect('main:dashboard')

    return render(request,'register.html')

# forgot password - /forgotpassword
# def forgot_pwd(request):
    # # check if user in session
    # if 'user_id' in request.session:
    #     return redirect('main:dashboard')

    # return render(request,'forgotpwd.html')
    # return redirect('/comingsoon')

# dashboard - /dashboard
def dashboard(request):
    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user
    }

    return render(request, 'dashboard.html',context)

# USER 

# settings - /settings

# AGENT

# listings - /agent/listing
def listings(request):
    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    if user_role != 'G' and user_role != 'A':
        return redirect('main:dashboard')
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    # get all listings
    listing = Listing.objects.all()

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user,
        'listing': listing
    }

    return render(request, 'listings.html',context)

# create listing - /agent/create
def create_listing(request):
    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    if user_role != 'G' and user_role != 'A':
        return redirect('main:dashboard')
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user
    }

    # return redirect('/comingsoon')
    return render(request, 'create_listing.html',context)

def agent_contact_listing(request):
    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    # get contact tickets
    get_contact = ContactTicket.objects.filter(contact_type='G')

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user,
        'get_contact': get_contact
    }

    return render(request, 'agent-contact-tickets.html',context)

# edit listing - /edit/:id
def edit_listing(request,listing_id):
    # check if listing exists
    listing_all = Listing.objects.values('id').all()
    found = False
    
    for id_list in listing_all:
        if id_list['id'] == int(listing_id):
            found = True
            break

    if not found:
        return redirect('main:listings')

    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    if user_role != 'G' and user_role != 'A':
        return redirect('main:dashboard')
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    listing = Listing.objects.get(id=listing_id)

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user,
        'listing': listing
    }

    return render(request, 'edit_listing.html',context)


# delete listing - /agent/delete/:id
def delete_listing(request, listing_id):
    # find listing and delete
    found_listing = Listing.objects.get(id=listing_id).delete()

    return redirect('main:listings')

# ADMIN

# users (view all users) - /admin/show
# create user - /admin/user
# activity - /admin/activity
# configure - /admin/config

# ticket - /admin/ticket
def ticket(request):
    check_session = False

    # check if user in session
    if 'user_id' not in request.session:
        return redirect('main:home')

    check_session = True
    show_dash_head = True

    # check user role
    user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    # get contact tickets
    get_contact = ContactTicket.objects.filter(contact_type='A')

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user,
        'get_contact': get_contact
    }

    return render(request, 'contact-tickets.html',context)

# catalog - /catalog
def search(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''

    list_of_states = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

    if len(request.GET['search']) != 0:
        message = 'Currently showing listings in: {}'.format(request.GET['search'])
        search = (request.GET['search']).split(', ')

        if len(search) == 4:
            # search database
            listing = Listing.objects.filter(addressOne__contains=search[0],city__contains=search[1],state__contains=search[2],zipcode=search[3])

            count = len(listing)
        elif len(search) == 3:
            # search database
            listing = Listing.objects.filter(city__contains=search[0],state__contains=search[1],zipcode=search[2])

            count = len(listing)
        elif len(search) == 1:
            listing = Listing.objects.filter(addressOne__contains=search[0])

            if len(listing) == 0:
                listing = Listing.objects.filter(city__contains=search[0])
                if len(listing) == 0:
                    listing = Listing.objects.filter(state__contains=search[0])

                    if len(listing) == 0:
                        for key in list_of_states:
                            if (key[1]).lower() == (search[0]).lower():
                                listing = Listing.objects.filter(state__contains=key[0])
                                break
                        if len(listing) == 0:
                            listing = Listing.objects.filter(zipcode=search[0])


            print listing
            count = len(listing)
        elif len(search) == 2:
            # city and state
            listing = Listing.objects.filter(city__contains=search[0],state__contains=search[1])
                
            # city and zip
            if len(listing) == 0:
                listing = Listing.objects.filter(city=search[0],zipcode=search[1])
                # state and zip
                if len(listing) == 0:
                    listing = Listing.objects.filter(state__contains=search[0],zipcode=search[1])

            count = len(listing)
        else:
            # get all listings
            listing = Listing.objects.values().all()
            message = ''
            count = len(listing)

    else:
        # get all listings
        listing = Listing.objects.values().all()
        message = ''
        count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Least Expensive
def leastExpensive(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('price')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Most Expensive
def mostExpensive(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('-price')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Recently Added
def recentlyAdded(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('-created_at')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Largest Interior
def largestInterior(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('-sq_footage')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Smallest Interior
def smallestInterior(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('sq_footage')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Most Bedrooms
def mostBedrooms(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('-bedrooms')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# Least Bedrooms
def leastBedrooms(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''


    # get all listings
    listing = Listing.objects.values().all().order_by('bedrooms')
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

def catalog(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''

    listing = Listing.objects.values().all()
    message = ''
    count = len(listing)
    
    arr = []
    listArr = []

    for l in listing:
        if len(arr) == 4:
            listArr.append(arr)
            arr = []

        arr.append(l)

    if len(arr) != 0:
        listArr.append(arr)
        arr = []
        
    print listArr

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user,
        'listing': listing,
        'message': message,
        'count': count,
        'listArr': listArr
    }

    return render(request,'catalog.html',context)

# contact us - /contact
def contact_us(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''
    
    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user
    }

    return render(request,'contactus.html',context)

# privacy - /privacy
def privacy(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
    
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
        print user
    else:
        user = ''

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user
    }

    return render(request,'privacy.html',context)

# terms of service - /termsofservice
def terms_of_service(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
    
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
        print user
    else:
        user = ''

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user
    }

    return render(request,'terms_of_service.html',context)

def coming_soon(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
    
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
        print user
    else:
        user = ''

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user': user
    }

    return render(request,'coming-soon.html',context)

def listing_details(request, listing_id):
    # check if listing exists
    listing_all = Listing.objects.values('id').all()
    found = False
    
    for id_list in listing_all:
        if id_list['id'] == int(listing_id):
            found = True
            break

    if not found:
        return redirect('main:listings')

    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True
        
    show_dash_head = False

    if check_session:
        # get user name
        user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
        user = '{} {}'.format(user_name['firstName'],user_name['lastName'])
    else:
        user = ''

    listing = Listing.objects.get(id=listing_id)

    context = {
        'show_head': show_dash_head,
        'check_session': check_session,
        'user': user,
        'listing': listing
    }

    return render(request, 'listing-details.html',context)

# Redirect/Logic

# logging in users - /user
def validatelogin(request):
    # validate users
    valid, result = User.objects.validateLogin(request.POST)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to login page 
        return redirect('main:login')   

    # store/print user in session
    request.session['user_id'] = result
    
    # check for type of user - user/admin/agent

    # redirect to dashboard accordingly
    return redirect('main:dashboard')

# register user - /create
def create(request):
    # validate users
    valid, result = User.objects.validateRegister(request.POST)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to registeration page 
        return redirect('main:register')

    # store/print user in session
    request.session['user_id'] = result

    # redirect to user dashboard
    return redirect('main:dashboard')

# logout user - /logout
def logout(request):
    # clear session
    request.session.clear()
    return redirect('main:home')

# new listing - /agent/create/new
def new_listing(request):
    # store user in session
    user = request.session['user_id']

    # get image path
    if len(request.FILES) == 0:
        uploaded_file_url = 'no image uploaded'
    else:
        # get image path
        myFile = request.FILES['thumbnail']
        fs = FileSystemStorage()
        filename = fs.save(myFile.name, myFile)
        uploaded_file_url = fs.url(filename)

    # validate listing
    valid, result = Listing.objects.create_listing(request.POST, user, uploaded_file_url)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to listing page
        return redirect('main:create_listing')

    return redirect('main:create_listing')

# update listing - /agent/edit/:id
def update_listing(request,listing_id):
    # store user in session
    user = request.session['user_id']

    if len(request.FILES) == 0:
        getListing = Listing.objects.values('image').get(id=listing_id)
        uploaded_file_url = (getListing['image']).split('\'')[0]
    else:
        # get image path
        myFile = request.FILES['thumbnail']
        fs = FileSystemStorage()
        filename = fs.save(myFile.name, myFile)
        uploaded_file_url = fs.url(filename)

    #  validate listing
    valid, result = Listing.objects.edit_listing(request.POST, listing_id, user, uploaded_file_url)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to listing page
        return redirect('/edit/{}'.format(listing_id))

    return redirect('main:listings')

def new_ticket(request):
    # get contact type
    type_contact = 'A'
    # validate ticket
    valid, result = ContactTicket.objects.validateTicket(request.POST, type_contact)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to registeration page 
        return redirect('main:contact_us')

    return redirect('main:contact_us')

def contact_agent_ticket(request,listing_id):
    # get contact type
    type_contact = 'G'
    # validate ticket
    valid, result = ContactTicket.objects.validateTicket(request.POST, type_contact)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        return redirect('/catalog/{}'.format(listing_id))

    return redirect('/catalog/{}'.format(listing_id))