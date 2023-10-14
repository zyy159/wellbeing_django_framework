from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from wellbeing_django_framework.exercise.signals import add_points

class AddPointsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/exercise/userprofile/':
            add_points(None, request.user, request)


class LocalhostOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip != '127.0.0.1':
            return HttpResponseForbidden('Forbidden: You can only access this from localhost')

        response = self.get_response(request)
        return response