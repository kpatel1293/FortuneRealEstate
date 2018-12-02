from django.conf.urls import url
from . import views
from django.conf import settings # IMAGE
from django.conf.urls.static import static # IMAGE

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

    url(r'^agent/listing$', views.listings, name='listings'),                       # listings          - /agent/listing
    url(r'^agent/create$', views.create_listing, name='create_listing'),            # create listing    - /agent/create
    url(r'^agent/conact-listing$', views.agent_contact_listing, name='agent_contact_listing'),
    url(r'^edit/(?P<listing_id>\d+)$', views.edit_listing, name='edit_listing'),
    url(r'^update/(?P<listing_id>\d+)$', views.update_listing, name='update_listing'),
    url(r'^agent/delete/(?P<listing_id>\d+)$', views.delete_listing, name='delete_listing'),

    # ADMIN

    # users (view all users) - /admin/show
    # url(r'^admin/show$', views.view_all_user, name='show_all_users'),
    # create user - /admin/user
    # activity - /admin/activity
    # configure - /admin/config
    url(r'^admin/ticket$', views.ticket, name='ticket'),                            # contact ticket    - /admin/ticket
    
    url(r'^search$', views.search, name='search'),                               # catalog           - /catalog

    url(r'^leastexpensive$', views.leastExpensive, name='least_expensive'),                    
    url(r'^mostexpensive$', views.mostExpensive, name='most_expensive'),                
    url(r'^recentlyadded$', views.recentlyAdded, name='recently_added'),                    
    url(r'^largestinterior$', views.largestInterior, name='largest_interior'),                    
    url(r'^smallestinterior$', views.smallestInterior, name='smallest_interior'),                    
    url(r'^mostbedrooms$', views.mostBedrooms, name='most_bedrooms'),                    
    url(r'^leastbedrooms$', views.leastBedrooms, name='least_bedrooms'),                    

    url(r'^catalog$', views.catalog, name='catalog'),                               # catalog           - /catalog    
    url(r'^catalog/(?P<listing_id>\d+)$', views.listing_details, name='listing_detail'),
    url(r'^catalog/(?P<listing_id>\d+)/ticket$', views.contact_agent_ticket, name='contact_agent_ticket'),
    url(r'^contact$', views.contact_us, name='contact_us'),                         # contact us        - /contact
    url(r'^privacy$', views.privacy, name='privacy'),                               # privacy           - /privacy
    url(r'^termsofservice$', views.terms_of_service, name='terms_of_service'),      # terms of service  - /termsofservice

    url(r'^user$', views.validatelogin, name='login-user'),                         # logging in users  - /user
    url(r'^create$', views.create, name='signup'),                                  # register user     - /create
    url(r'^logout$', views.logout, name='logout'),                                  # logout user       - /logout
    url(r'^agent/create/new$', views.new_listing, name='new_listing'),              # new listing       - /agent/create/new
    
    url(r'^newticket$', views.new_ticket, name='new_ticket')                       # new ticket        - /newticket
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)