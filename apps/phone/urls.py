from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm
from phone import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='phone-index'),
)
