try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.utils.functional import lazy
    from django.core.urlresolvers import reverse

    # ref: http://djangosnippets.org/snippets/2445/
    reverse_lazy = lambda name=None, *args : lazy(reverse, str)(name, args=args)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'website.Member'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('website:login_url')
LOGOUT_URL = reverse_lazy('website:logout_url')

ANONYMOUS_USER_ID = -1

CURRENT_YEAR = 2010
