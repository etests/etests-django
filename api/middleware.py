from django.utils.deprecation import MiddlewareMixin


class PrintMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request)
        return None
