from django.shortcuts import render,redirect

# Create your views here.
# index - /
# render template
def index(request):
    return render(request,'index.html')