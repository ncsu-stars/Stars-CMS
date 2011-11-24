try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.utils.functional import lazy
    from django.core.urlresolvers import reverse

    # ref: http://djangosnippets.org/snippets/2445/
    reverse_lazy = lambda name=None, *args : lazy(reverse, str)(name, args=args)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ncsu.wrap.backends.WrapBackend',
)

AUTH_PROFILE_MODULE = 'cms.Member'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('cms:login_url')
LOGOUT_URL = reverse_lazy('cms:logout_url')

ANONYMOUS_USER_ID = -1

CURRENT_YEAR = 2010

# Remove in production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Can be set to any email
DEFAULT_FROM_EMAIL = 'donotrespond@stars.csc.ncsu.edu'

# Used for now to get the SLC leader
SLC_LEADER = 'Arpan Chakraborty'
