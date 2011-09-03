from django.conf import settings

def accounts(request):
    '''
    Provides the ``authentication`` dictionary context variable containing
    details about the current authentication method used by the currently
    logged in user.

    Details about the ``authentication`` dictionary:

    If the user is logged in, this context variable is dictionary with the
    following keys:

    * ``method`` - Authentication method used to log in. Set to '``twitter``' for
      Twitter, '``facebook``' for Facebook or '``django.contrib.auth``' if user logs in via
      Django's default authentication mechanism.

    * ``name`` - Display name of the currently logged in user. Set to '``@twitterid``'
      for Twitter, '``first_name``' for Facebook, or '``request.user.username``' for
      Django.contrib.auth.

    If the user is not logged in, this context variable is ``None``. 

    '''

    authentication = request.session.get('authentication')
    if authentication is None and request.user.is_authenticated():
        authentication = dict(
            method='django.contrib.auth',
            name=request.user.username,
        )

    return dict(
        authentication=authentication,
    )

