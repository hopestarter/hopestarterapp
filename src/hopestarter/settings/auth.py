
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_INSTALLED_APPS = (
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.twitter',
)

LOGIN_REDIRECT_URL = '/partners/vetting/'

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False

ACCOUNT_ADAPTER = 'hopebase.account.AccountAdapter'

ACCOUNT_SIGNUP_FORM_CLASS = 'hopebase.forms.SignupForm'

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
