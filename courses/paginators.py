from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """Пагинация для курсов"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class LessonPagination(PageNumberPagination):
    """Пагинация для уроков"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SubscriptionPagination(PageNumberPagination):
    """Пагинация для подписок"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
