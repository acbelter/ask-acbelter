from django.conf.urls import url

from django.contrib.auth.views import login, logout_then_login
import users.views


urlpatterns = [
    url(r'^user/(?P<user_id>\d+)$', users.views.user_details, name="user-details"),
    url(r'^login/$', login, name="login"),
    url(r'^register/$', users.views.register, name="register"),
    url(r'^settings/$', users.views.settings, name="settings"),
    url(r'^logout/$', logout_then_login, name="logout"),
]
