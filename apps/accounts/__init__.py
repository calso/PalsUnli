def post_auth_redirect(request):
    from django.core.urlresolvers import reverse as url_for_view
    from django.http import HttpResponseRedirect

    if request.GET.get('next', None):
        request.session['POST_AUTH_URL'] = request.GET.get('next')
    return_url = request.session.get('POST_AUTH_URL')
    if return_url is None:
        return_url = url_for_view('accounts-postauthcmd')
    return HttpResponseRedirect(return_url)
