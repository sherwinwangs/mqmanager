from django.conf.urls import url
from .views import *

app_name = 'users'

urlpatterns = [
    # Login
    url(r'^login$', user_login, name='user-login'),
    url(r'^logout$', user_logout, name='user-logout'),

    # User
    url(r'^user$', user_logout, name='user-list'),
    url(r'^user/create$', user_logout, name='user-list'),
    url(r'^user/delete$', user_logout, name='user-list'),

    # Profile
    url(r'^profile/$', user_login, name='user-profile'),
]
