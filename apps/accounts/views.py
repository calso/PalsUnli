from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext, ugettext_lazy as _

import datetime

import accounts
from accounts.forms import LoginForm

def index(request):
    '''
    This view is used as the 'dashboard' for user account functions.

    * URL Name

      ``accounts-index``

    * Available Context

      ``in_account_home`` - Always set to ``True`` when we are in this view.

    * Template

      'accounts/index.html'

    '''
    context = dict(in_account_home=True)

    return render_to_response(
        'accounts/index.html',
        context,
        context_instance=RequestContext(request)
    )

def postauthcmd(request):
    '''
    This view is called after a successful login or logout.

    * URL Name

      ``accounts-postauthcmd``

    * Available Context

      - ``post_auth_url`` - Taken from POST_AUTH_URL which is set by
        accounts.decorators.require_login.  Defaults to
        settings.WEBSITE_DEFAULT_VIEW if not found.

      - ``auth_logged_out`` - Is set to True if called from the logout view.

    * Template

      'accounts/postauthcmd.html'

    '''
    from django.core.urlresolvers import reverse as url_for_view

    context = dict()
    if request.session.get('POST_AUTH_URL'):
        context['post_auth_url'] = request.session['POST_AUTH_URL']
        del request.session['POST_AUTH_URL']
    else:
        context['post_auth_url'] = getattr(settings, 'WEBSITE_DEFAULT_VIEW', '/')

    if request.session.get('AUTH_LOGGED_OUT'):
        context['auth_logged_out'] = request.session['AUTH_LOGGED_OUT']
        del request.session['AUTH_LOGGED_OUT']
    
    if request.session.get('is_new_user_account'):
        context['is_new_user_account'] = request.session['is_new_user_account']
        del request.session['is_new_user_account']
   
    return render_to_response(
        'accounts/postauthcmd.html',
        context,
        context_instance=RequestContext(request)
    )

def login(request, template_name='signin.html'):
    if request.GET.get('next', None):
        request.session['POST_AUTH_URL'] = request.GET.get('next')
    if 'POST' == request.method:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            if form.cleaned_data['keep_signed_in']:
                # Sessions expire in about ten years.
                request.session.set_expiry(datetime.timedelta(3650))
            else:
                # Session expires when user closes browser.
                request.session.set_expiry(0)
            if request.GET.get('ajax'):
                pass
                '''
                from utils import json
                return HttpResponse(
                    json.get_json(
                        request,
                        200,
                        ugettext(u'Login successful.'),
                        dict()
                    ),
                    content_type=json.get_response_mimetype(request)
                )
                '''
            else:
                return accounts.post_auth_redirect(request)
        else:
            if request.GET.get('ajax'):
                pass
                '''
                from utils import json
                return HttpResponse(
                    json.get_json(
                        request,
                        403,
                        ugettext(u'Authentication Failed. Access forbidden.'),
                        dict()
                    ),
                    content_type=json.get_response_mimetype(request)
                )
                '''
    else:
        form = LoginForm()

    context = dict(
        form=form
    )

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )

def logout(request):
    '''
    This view will log out the currently logged in user.

    * URL Name

      ``accounts-logout``

    * Available Context

      None.

    * Template

      None.

    '''
    from django.contrib.auth import logout

    logout(request)

    if request.session.get('authentication'):
        del request.session['authentication']

    request.session['AUTH_LOGGED_OUT'] = True

    return accounts.post_auth_redirect(request)

def edit(request):
    '''
    This view is used for editing user profile and account details. This will
    allow users to specify a custom username in place of the one assigned by
    the system to them when their account was created either via Twitter or
    Facebook.

    * URL Name

      ``accounts-edit``

    * Available Context

      ``form`` - ModelForm object for editing the user account details.

    * Template

      'accounts/edit.html'

    '''
    from forms import UserAccountForm

    if 'POST' == request.method:
        form = UserAccountForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message=u'Account details updated.')
        else:
            request.user.message_set.create(message=u'The form you submitted contained errors. Please correct them and submit the form again.')
    else:
        form = UserAccountForm(instance=request.user)

    context = dict(
        form=form
    )

    return render_to_response(
        'accounts/edit.html',
        context,
        context_instance=RequestContext(request)
    )

def user_details(request, userid):
    '''
    Display information about a particular user.

    * URL Name

      ``accounts-user-details``

    * Available Context

      ``user`` - User obejct for the requested page.

      ``on_user_details_page`` - Always set to ``True`` when we are in this view.

    * Template

      'accounts/details.html'

    '''
    user = get_object_or_404(User, pk=long(userid))
    context = dict(
        user=user,
        on_user_details_page=True,
    )
    return render_to_response(
        'accounts/details.html',
        context,
        context_instance=RequestContext(request)
    )

def user_confirm_email(request, useridb36=None, token=None):
    '''
    Confirms a user's email account.

    * URL Name

      ``accounts-user-confirm-email``

    * Available Context

      - ``valid_link`` - Set to either ``True`` or ``False`` depending on how
        validation of ``useridb36`` and ``token`` went on.

    * Template

      'accounts/user_confirm_email.html'

    '''
    assert useridb36 is not None and token is not None
    try:
        userid = base36_to_int(useridb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, pk=userid)

    profile = user.get_profile()
    if profile.email_confirmed:
        raise Http404

    context = dict(
        valid_link=False,
        user=user,
    )

    if token_generator.check_token(user, token):
        context['valid_link'] = True
        profile.email_confirmed = True
        profile.save()

    return render_to_response(
        'accounts/user_confirm_email.html',
        context,
        context_instance=RequestContext(request)
    )
