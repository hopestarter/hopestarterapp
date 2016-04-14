from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'mark': reverse('collector:user_marks', request=request, format=format),
        'marks': reverse('collector:locationmark', request=request, format=format),
        'uploadimage': reverse('collector:uploadimage', request=request, format=format),
        'user': reverse('base:account', request=request, format=format)
    })
