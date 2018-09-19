from django.shortcuts import render,redirect

# Create your views here.

# home - /
# render template
def home(request):
    return render(request,'index.html')

# login - /login
# render template
def login(request):
    pass

# registration - /register
# render template
def register(request):
    pass
