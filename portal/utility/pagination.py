from rest_framework.pagination import PageNumberPagination
from Job_Portal.settings import base


class Pagination(PageNumberPagination):
    page_size = getattr(base, 'PAGINATION_PAGE_SIZE', 5)
