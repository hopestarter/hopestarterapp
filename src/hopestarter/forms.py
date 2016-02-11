from django import forms


class SignupForm(forms.Form):
    ethnicity = forms.CharField(label="ethnicity")

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass
