from django.conf.urls import url
from . import views

urlpatterns = [
    # TEMPLATES
    url(r'^$', views.home, name='home'),                                            # home page         - /
    url(r'^login$', views.login, name='login'),                                     # login page        - /login
    url(r'^register$', views.register, name='register'),                            # register page     - /register
    url(r'^forgotpassword$', views.forgot_pwd, name='forgot_pwd'),                  # forgot password   - /forgotpassword
    url(r'^dashboard$', views.dashboard, name='dashboard'),                         # dashboard  - /dashboard
    url(r'^catalog$', views.catalog, name='catalog'),                               # catalog           - /catalog
    url(r'^contact$', views.contact_us, name='contact_us'),                         # contact us        - /contact
    url(r'^privacy$', views.privacy, name='privacy'),                               # privacy           - /privacy
    url(r'^termsofservice$', views.terms_of_service, name='terms_of_service'),      # terms of service  - /termsofservice

    url(r'^user$', views.validatelogin, name='login-user'),                         # logging in users  - /user
    url(r'^create$', views.create, name='signup'),                                  # register user     - /create
    url(r'^logout$', views.logout, name='logout')                                   # logout user       - /logout
]
