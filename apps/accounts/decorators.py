from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as url_for_view

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

def require_login(the_view, ajax=False, login_url_name='accounts-login'):
    def _require_login(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['POST_AUTH_URL'] = request.get_full_path()
            if ajax:
                return the_view(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(url_for_view(login_url_name))
        else:
            return the_view(request, *args, **kwargs)
    return wraps(the_view)(_require_login)
