# config/middleware.py
from django.utils.deprecation import MiddlewareMixin


class ForceUTF8Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Устанавливаем кодировку UTF-8 для JSON-ответов
        content_type = response.get('Content-Type', '')

        if 'application/json' in content_type:
            response['Content-Type'] = 'application/json; charset=utf-8'
        elif content_type.startswith('text/'):
            response['Content-Type'] = content_type + '; charset=utf-8'

        return response