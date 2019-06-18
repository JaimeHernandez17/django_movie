from django.contrib.auth import logout
from django.shortcuts import redirect

from appMovie.models import TokenUser
from django.contrib.auth.models import User


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.META.get('HTTP_AUTHORIZATION'):
                token = request.META.get('HTTP_AUTHORIZATION')
                token = TokenUser.objects.get(token=token)
                request.user = token.user
            if not request.user.is_anonymous:
                TokenUser.objects.get(user=request.user)

        except Exception:
            logout(request)
            response = redirect('logout')
            response.delete_cookie('user_location')
            return response
            pass

        response = self.get_response(request)
        return response
