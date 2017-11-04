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

    # users view
    url(r'^users[/]?$', api.users.dispatcher),
    url(r'^users/(?P<username>[\w\.\-_]+)$', api.users.dispatcher),
    url(r'^users/(?P<username>[\w\.\-_]+)/(?P<attributes>[\w]+)$', api.users.dispatcher),

    # Administration view
    # url(r'^admin/$', views.admin_dispatcher),
    # url(r'^admin/users', views.admin_users_dispatcher),

    # Policies view
    url(r'^policies', views.policies),

    # logs view
    # url(r'^logs$', views.logs_dispatcher),

    # Registration view
    # url(r'^register', api.register.dispatcher),

    # Watcha view
    # url(r'^attributes', views.attributes_dispatcher),
    # url(r'^action', views.activate_user),
    # url(r'^logged', views.user_is_authenticate),
    # url(r'^isGroupAdmin', views.user_is_group_admin),
    # url(r'^isAdmin', views.user_is_admin),
    # url(r'^groupAdmin/$', views.groups_dispatcher),
    # url(r'^groupAdmin/[\w]+', views.group_dispatcher),
]
