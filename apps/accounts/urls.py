from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm
from accounts import views

urlpatterns = patterns(
    '',
    url(r'^edit/$', views.edit, name='accounts-edit'),
    url(r'^logout/$', views.logout, name='accounts-logout'),
    url(r'^login/$', views.login, name='accounts-login'),
    url(r'^password/reset/done/$', password_reset_done, {'template_name': 'accounts/password_reset_done.html'},name="password-reset-done"),
    url(r'^password/reset/$', password_reset,{'template_name': 'accounts/password_reset.html','email_template_name':'accounts/password_reset_email.html'},name="password-reset"),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$',password_reset_confirm,{'template_name':'accounts/password_reset_confirm.html'},name="password-reset-confirm"),
    url(r'^password/reset/complete/$','django.contrib.auth.views.password_reset_complete',{'template_name':'accounts/password_reset_complete.html'}),
    url(r'^postauthcmd/$', views.postauthcmd, name='accounts-postauthcmd'),
    url(r'^$', views.index, name='accounts-index'),
    url(r'^details/(?P<userid>\d+)/$', views.user_details, name='accounts-details'),
    url(r'^confirm-email/(?P<useridb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.user_confirm_email, name='accounts-user-confirm-email'),
)
