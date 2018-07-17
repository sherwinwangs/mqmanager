"""mqmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from .views import dashboard, page_not_found, page_error, permission_denied

# from django.contrib import admin
urlpatterns = [
    # dashboard
    url(r'^$', dashboard, name='dashboard'),

    # mq
    url(r'^mq/', include("rabbitmq.urls")),
    url(r'^users/', include("users.urls")),
]

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error
