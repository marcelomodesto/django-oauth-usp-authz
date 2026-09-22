from django.contrib.auth.backends import ModelBackend
from django_oauth_usp_authz.models import UsuarioAutorizado


class OAuthUSPAuthzBackend(ModelBackend):
    """
    Backend que verifica se o usuário autenticado via django-oauth-usp
    está na lista de autorizados. Superusuários sempre têm acesso.
    """

    def authenticate(self, request, **kwargs):
        user = super().authenticate(request, **kwargs)

        if user is None:
            return None

        if user.is_superuser:
            return user

        if not UsuarioAutorizado.objects.filter(
            numero_usp=user.login,
            ativo=True
        ).exists():
            return None

        return user
