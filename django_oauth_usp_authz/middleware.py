from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django_oauth_usp.accounts.middleware import OAuthUspMiddleware
from django_oauth_usp_authz.models import UsuarioAutorizado


class OAuthUSPAuthzMiddleware(OAuthUspMiddleware):
    """
    Middleware que estende OAuthUspMiddleware com verificação de autorização.
    Verifica a cada request se o usuário ainda está na lista de autorizados.
    Superusuários são isentos da verificação.
    """

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        if request.user.is_authenticated:
            if not UsuarioAutorizado.objects.filter(
                numero_usp=request.user.login,
                ativo=True
            ).exists():
                logout(request)
                return redirect(settings.LOGIN_URL)

        return super().__call__(request)
