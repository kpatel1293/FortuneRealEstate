from django.conf.urls import url
from . import views

urlpatterns = [
    # TEMPLATES
    url(r'^comingsoon$', views.coming_soon, name='coming_soon'),                     # coming soon page  - /comingsoon    
    url(r'^$', views.home, name='home'),                                            # home page         - /
    url(r'^login$', views.login, name='login'),                                     # login page        - /login
    url(r'^register$', views.register, name='register'),                            # register page     - /register
    # url(r'^forgotpassword$', views.forgot_pwd, name='forgot_pwd'),                  # forgot password   - /forgotpassword
    url(r'^dashboard$', views.dashboard, name='dashboard'),                         # dashboard         - /dashboard
    # USER 

    # settings - /settings

    # AGENT

    # url(r'^agent/listing$', views.listings, name='listings'),                       # listings          - /agent/listing
    # url(r'^agent/create$', views.create_listing, name='create_listing'),            # create listing    - /agent/create

    # ADMIN

    # users (view all users) - /admin/show
    # create user - /admin/user
    # activity - /admin/activity
    # configure - /admin/config
    url(r'^admin/ticket$', views.ticket, name='ticket'),                            # contact ticket    - /admin/ticket
    
    # url(r'^catalog$', views.catalog, name='catalog'),                               # catalog           - /catalog
    url(r'^contact$', views.contact_us, name='contact_us'),                         # contact us        - /contact
    # url(r'^privacy$', views.privacy, name='privacy'),                               # privacy           - /privacy
    # url(r'^termsofservice$', views.terms_of_service, name='terms_of_service'),      # terms of service  - /termsofservice

    url(r'^user$', views.validatelogin, name='login-user'),                         # logging in users  - /user
    url(r'^create$', views.create, name='signup'),                                  # register user     - /create
    url(r'^logout$', views.logout, name='logout'),                                  # logout user       - /logout
    # url(r'^agent/create/new$', views.new_listing, name='new_listing'),              # new listing       - /agent/create/new
    
    url(r'^newticket$', views.new_ticket, name='new_ticket')                        # new ticket        - /newticket
]
