from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([('result',data)]))