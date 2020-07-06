"""github_auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^merge_request_update/(?P<merge_request_id>[0-9])/(?P<status>[-\w]+)/$', views.merge_request_update, name='merge-request-update'),
    url(r'^merge_request/(?P<merge_request_id>[0-9])/$', views.merge_request, name='merge-request'),
    url(r'^merge_request', views.merge_request, name='merge-request'),
    url('', views.home, name='home'),
]
