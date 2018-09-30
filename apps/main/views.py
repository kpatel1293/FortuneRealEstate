from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

# Create your views here.

# Render Templates

# home - /
def home(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True

    context = {
        'check_session': check_session
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
def forgot_pwd(request):
    # check if user in session
    if 'user_id' in request.session:
        return redirect('main:dashboard')

    return render(request,'forgotpwd.html')

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
# create listing - /agent/create

# ADMIN

# users (view all users) - /admin/show
# create user - /admin/user
# activity - /admin/activity
# configure - /admin/config


# catalog - /catalog
def catalog(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True

    context = {
        'check_session': check_session
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

    context = {
        'check_session': check_session
    }

    return render(request,'privacy.html',context)

# terms of service - /termsofservice
def terms_of_service(request):
    check_session = False
    # check if user in session
    if 'user_id' in request.session:
        check_session = True

    context = {
        'check_session': check_session
    }

    return render(request,'terms_of_service.html',context)

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