from .base import *

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

if 'django.contrib.sites' not in INSTALLED_APPS:
	INSTALLED_APPS += ('django.contrib.sites',)

INSTALLED_APPS += (
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.twitter',
)

LOGIN_REDIRECT_URL = 'home'

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False

ACCOUNT_ADAPTER = 'hopestarter.account.AccountAdapter'

ACCOUNT_SIGNUP_FORM_CLASS = 'hopestarter.forms.SignupForm'

