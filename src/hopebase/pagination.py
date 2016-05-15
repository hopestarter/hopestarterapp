__author__ = 'mpetyx'

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Used for pagination in api view using parameter `page_size_query_param`=size
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
