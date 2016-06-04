from django import forms
from django.conf import settings


class SignupForm(forms.Form):
    ethnicity = forms.CharField(label="Ethnicity",
                                max_length=settings.ETHNICITY_MAX_NAME)
    name = forms.CharField(
        label="First name", max_length=settings.NAME_MAX, required=False)
    surname = forms.CharField(
        label="Last name", max_length=settings.NAME_MAX, required=False)
    picture = forms.URLField(
        label="Profile picture URL", required=False)
    bitcoin = forms.CharField(label="Bitcoin", max_length=100, required=False)

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass
