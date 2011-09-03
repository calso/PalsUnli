from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.api_views',
                       url(r'^v1.0/check-username/$', 'check_username', name='api-accounts-check-username'),
                       url(r'^v1.0/check-email/$', 'check_email', name='api-accounts-check-email'),
                      )
