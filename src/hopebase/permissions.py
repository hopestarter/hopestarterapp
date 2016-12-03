from oauth2_provider.ext.rest_framework import (
    OAuth2Authentication, TokenHasScope, TokenHasResourceScope
)
from rest_framework.permissions import *   # noqa


class WeakTokenMixin(object):

    """
    The request is authenticated as a user if the token
    exists it has the right scope or if it was already authenticated.
    """

    def has_permission(self, request, view):
        if request.successful_authenticator != OAuth2Authentication:
            return True
        return super(WeakTokenMixin, self).has_permission(request, view)


class WeakTokenHasScope(WeakTokenMixin, TokenHasScope):
    pass


class WeakTokenHasResourceScope(WeakTokenMixin, TokenHasResourceScope):
    pass
