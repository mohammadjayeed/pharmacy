from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    # please chnage page size as according to need
    page_size = 3 

    