from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework.permissions import *

class OptionalTokenHasScope(TokenHasScope):
    """
    The request is authenticated as a user and if the token
    exists it has the right scope.
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return True
        return super(OptionalTokenHasScope, self).has_permission(request, view)
