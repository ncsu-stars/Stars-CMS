import os

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
SLC_LEADERS = [ 'Arpan Chakraborty', 'Kristy Boyer']

SPONSOR_LOGO_URL = 'images/logos/sponsors/'
SPONSORS = [ dict(zip(['name', 'logo_path'], x)) for x in [
                ('Deutsche Bank Global Technology', 'dbgt.jpg'),
                ('NetApp', 'netapp.jpg'),
                ('SAS', 'sas.jpg'),
                ('EMC', 'emc.jpg'),
                ('Cisco', 'cisco.jpg'),
                ('Duke Energy', 'duke_energy.jpg'),
                ('Tekelec', 'tekelec.jpg'),
                ('I-Cubed', 'i-cubed.jpg'),
                ('TCS', 'tcs.jpg'),
                ('Lowes\'s Companies', 'lowes.jpg'),
                ] ]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.pages',
)
