"""openstack_register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from registration import views, api

urlpatterns = [  # pylint: disable=invalid-name
    # home view
    url(r'^$', views.home),

    # login / logout view
    url(r'^login', views.login),
    url(r'^logout', views.logout),

    # /users view
    url(r'^users[/]?$', api.users.dispatcher),
    url(r'^users/(?P<username>[\w\.\-_]+)$', api.users.dispatcher),
    url(r'^users/(?P<username>[\w\.\-_]+)/(?P<attributes>[\w]+)$', api.users.dispatcher),

    # /groups view
    url(r'^groups[/]?$', api.groups.dispatcher),
    url(r'^groups/(?P<group>[\w\.\-_]+)$', api.groups.dispatcher),
    url(r'^groups/(?P<group>[\w\.\-_]+)/(?P<attribute>[\w]+)$', api.groups.dispatcher),
    url(r'^groups/(?P<group>[\w\.\-_]+)/(?P<attribute>[\w]+)/(?P<value>[\w\.\-_]+)$',
        api.groups.dispatcher),

    # Policies view
    url(r'^policies', views.policies),

    # logs view
    # url(r'^logs$', views.logs_dispatcher),
]
