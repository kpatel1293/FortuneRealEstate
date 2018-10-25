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
# def listings(request):
    # check_session = False

    # # check if user in session
    # if 'user_id' not in request.session:
    #     return redirect('main:home')

    # check_session = True
    # show_dash_head = True

    # # check user role
    # user_role = User.objects.values('permissionLevel').get(id=request.session['user_id'])['permissionLevel']
    # if user_role != 'G':
    #     return redirect('main:dashboard')
    
    # # get user name
    # user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    # user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    # # get all listings
    # # listing = Listing.objects.values().all()
    # # print listing

    # context = {
    #     'check_session': check_session,
    #     'show_head': show_dash_head,
    #     'user_role': user_role,
    #     'user': user,
    #     # 'listing': listing
    # }

    # return redirect('/comingsoon')
    # return render(request, 'listings.html',context)

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
    if user_role != 'G':
        return redirect('main:dashboard')
    
    # get user name
    user_name = User.objects.values('firstName', 'lastName').get(id=request.session['user_id'])
    user = '{} {}'.format(user_name['firstName'],user_name['lastName'])

    print Listing.objects.all()

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user
    }

    # return redirect('/comingsoon')
    return render(request, 'create_listing.html',context)

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
    get_contact = ContactTicket.objects.all()
    print get_contact

    context = {
        'check_session': check_session,
        'show_head': show_dash_head,
        'user_role': user_role,
        'user': user,
        'get_contact': get_contact
    }

    return render(request, 'contact-tickets.html',context)

# catalog - /catalog
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

    if len(request.GET['search']) != 0:
        message = 'Currently showing listings in: {}'.format(request.GET['search'])
        search = (request.GET['search']).split(', ')

        if len(search) == 3:
            # search database
            listing = Listing.objects.filter(city=search[0],state=search[1],zipcode=search[2])

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
        if len(arr) == 3:
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
    # return redirect('/comingsoon')

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
# def privacy(request):

    # check_session = False
    # # check if user in session
    # if 'user_id' in request.session:
    #     check_session = True

    # context = {
    #     'check_session': check_session
    # }

    # return render(request,'privacy.html')
    # return redirect('/comingsoon')

# terms of service - /termsofservice
# def terms_of_service(request):
    # check_session = False
    # # check if user in session
    # if 'user_id' in request.session:
    #     check_session = True

    # context = {
    #     'check_session': check_session
    # }
    
    # return render(request,'terms_of_service.html',context)
    # return redirect('/comingsoon')

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

# Redirect/Logic

# logging in users - /user
def validatelogin(request):
    # validate users
    valid, result = User.objects.validateLogin(request.POST)

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
            print e
        # if there are errors return back to login page 
        return redirect('main:login')   

    # store/print user in session
    request.session['user_id'] = result
    print request.session['user_id']
    
    # check for type of user - user/admin/agent

    # redirect to dashboard accordingly
    return redirect('main:dashboard')

# register user - /create
def create(request):
    # validate users
    valid, result = User.objects.validateRegister(request.POST)

    print valid

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to registeration page 
        return redirect('main:register')

    # store/print user in session
    request.session['user_id'] = result
    print request.session['user_id']

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
    myFile = request.FILES['thumbnail']
    fs = FileSystemStorage()
    filename = fs.save(myFile.name, myFile)
    uploaded_file_url = fs.url(filename)
    print uploaded_file_url

    # validate listing
    valid, result = Listing.objects.create_listing(request.POST, user, uploaded_file_url)

    print valid

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to listing page
        return redirect('main:create_listing')

    return redirect('main:create_listing')

def new_ticket(request):
    # validate users
    valid, result = ContactTicket.objects.validateTicket(request.POST)

    print valid

    # check for errors
    if not valid:
        for e in result:
            messages.error(request, e)
        # if there are errors return back to registeration page 
        return redirect('main:contact_us')

    return redirect('main:contact_us')

# def search(request):
#     return redirect('main:catalog')
