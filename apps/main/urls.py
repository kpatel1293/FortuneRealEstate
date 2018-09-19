from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),                        # home page ('/')
    url(r'^login^$', views.login, name='login'),                # login page ('/login')
    url(r'^register^$', views.register, name='register'),       # register page ('/register')
]
