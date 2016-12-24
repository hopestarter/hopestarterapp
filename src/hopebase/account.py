from django.core.urlresolvers import reverse
from django.db import transaction

from allauth.account.adapter import DefaultAccountAdapter

from hopespace.models import Ethnicity, EthnicMember
from hopebase.models import UserProfile


class AccountAdapter(DefaultAccountAdapter):

    def _associate_ethnicity(self, user, ethnicity):
        ethnicity, _ = Ethnicity.objects.get_or_create(name=ethnicity)
        EthnicMember(person=user, ethnicity=ethnicity).save()

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(
            request, user, form, commit=False)
        profile = {
            'user': user,
            'name': form.cleaned_data.get('name', None),
            'surname': form.cleaned_data.get('surname', None),
            'picture': form.cleaned_data.get('picture', None),
            'bitcoin': form.cleaned_data.get('bitcoin', None),
        }
        with transaction.atomic():
            user.save()
            UserProfile.objects.create(**profile)
            if 'ethnicity' in form.cleaned_data:
                self._associate_ethnicity(
                    user, form.cleaned_data['ethnicity'])

    def get_login_redirect_url(self, request):
        if request.user.involved.filter(revoked=None).first() is None:
            return "/"
        return reverse('vetting')
