from django.conf import settings
from django.http import HttpResponse


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.MAINTENANCE_MODE and not request.path.startswith('/admin/'):
            return HttpResponse('Maintenance Mode')

        response = self.get_response(request)
        return response

