from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 20  # Set the number of items per page
    page_size_query_param = 'page_size'  # Allow clients to override the page size
    max_page_size = 500  # Limit the maximum page size that can be requested
