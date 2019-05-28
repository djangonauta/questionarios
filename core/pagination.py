"""Paginadores da aplicação core."""

from rest_framework import pagination, response


class CorePaginator(pagination.PageNumberPagination):
    """Paginador com chaves extras."""

    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        """Inclui chaves extras na resposta."""
        return response.Response({
            'count': self.page.paginator.count,
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
            'results': data,
            'page_range': list(self.page.paginator.page_range),
            'num_pages': self.page.paginator.num_pages,
            'per_page': self.page.paginator.per_page,
            'number': self.page.number,
            'next_page_number': self.page.next_page_number() if self.page.has_next() else None,
            'previous_page_number': self.page.previous_page_number() if self.page.has_previous() else None,
        })
