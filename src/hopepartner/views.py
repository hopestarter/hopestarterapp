import json

from django.db import transaction
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from hopebase.models import UserProfile, Vetting
from hopepartner.log import logger


user_model = get_user_model()


@require_http_methods(["GET", "POST"])
def vetting(request):
    user = request.user
    if not user.is_authenticated():
        messages.error(request, _("You must login first."))
        return redirect(reverse('account_login'))

    try:
        reviewer = user.involved.filter(revoked=None).first()
        if reviewer is None:
            raise PermissionDenied
        org = reviewer.organization
    except ObjectDoesNotExist:
        raise PermissionDenied

    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            if "id" not in data or "status" not in data:
                rsp = json.dumps({"error": True, "msg": "invalid request"})
                return HttpResponse(
                    rsp, status=400, content_type='application/json')

            user_id = data["id"]
            new_status = data["status"]
            if new_status == "vetted":
                with transaction.atomic():
                    subject = user_model.objects.get(id=user_id)
                    vet = Vetting(
                        subject=subject, reviewer=reviewer,
                        organization=org)
                    vet.save()
                data = {"error": False, "msg": "created"}
            elif new_status == "unvetted":
                vets = Vetting.objects.filter(
                    subject__id=user_id, reviewer=reviewer, revoked=None)
                n = vets.update(revoked=timezone.now())
                data = {"error": False, "msg": "revoked", "count": n}
            return HttpResponse(
                json.dumps(data), content_type='application/json')
        except user_model.DoesNotExist:
            rsp = json.dumps({"error": True, "msg": "user not found"})
            return HttpResponse(
                rsp, status=400, content_type='application/json')
        except Exception as e:
            logger.exception(
                "Error handling vet request from user %s", user.username)
            rsp = json.dumps({"error": True, "msg": str(e)})
            return HttpResponse(
                rsp, status=500, content_type='application/json')

    profiles = UserProfile.objects.filter(signup='app')
    profiles = profiles.prefetch_related('user__vetting_set')
    return render(request, "vetting.html", context={
        'object_list': profiles
    })
