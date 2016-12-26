from django.utils import timezone

from .models import Visitor


class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            visitor, _ = Visitor.objects.get_or_create(user=request.user)
            visitor.last_seen = timezone.now()
            visitor.save()

        return response
