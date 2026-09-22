# django-oauth-usp-authz

Controle de acesso por lista de usuários autorizados para aplicações Django que utilizam `django-oauth-usp`.

## Funcionalidades

- **Modelo `UsuarioAutorizado`** — Lista de usuários autorizados a acessar o sistema
- **Backend `OAuthUSPAuthzBackend`** — Verificação de autorização durante autenticação
- **Middleware `OAuthUSPAuthzMiddleware`** — Verificação contínua de autorização a cada request
- **Admin integrado** — Interface para gerenciar usuários autorizados (ativar/desativar)

## Regras de negócio

1. **Superusuários locais sempre têm acesso** — Não passam pela verificação de lista
2. **Usuários da USP precisam estar na lista** — O número USP deve existir em `UsuarioAutorizado` com `ativo=True`
3. **Revogação imediata** — Desativar um usuário na lista Admin faz ele perder acesso na próxima requisição, mesmo que já esteja logado

## Instalação

```bash
pip install django-oauth-usp-authz
```

## Configuração

Adicione `django_oauth_usp_authz` ao `INSTALLED_APPS` **após** `django_oauth_usp.accounts`:

```python
INSTALLED_APPS = [
    ...
    'django_oauth_usp.accounts',
    'django_oauth_usp_authz',
    ...
]
```

Configure o backend de autenticação:

```python
AUTHENTICATION_BACKENDS = [
    'django_oauth_usp_authz.backends.OAuthUSPAuthzBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

Configure o middleware **após** `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
    'django_oauth_usp_authz.middleware.OAuthUSPAuthzMiddleware',
    ...
]
```

Execute as migrations:

```bash
python manage.py migrate
```

## Uso

### Gerenciando usuários autorizados

Acesse o Django Admin em `/admin/` e procure por "Usuários Autorizados".

Na listagem é possível:
- **Ativar/desativar** usuários diretamente (coluna "Ativo")
- **Buscar** por número USP ou observação
- **Filtrar** por status (ativo/inativo)

### Protegendo views

Todas as views que utilizam `LoginRequiredMixin` já estão protegidas:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class MinhaView(LoginRequiredMixin, View):
    ...
```

### Verificação manual

Para verificar se um usuário está autorizado:

```python
from django_oauth_usp_authz.models import UsuarioAutorizado

def esta_autorizado(user):
    if user.is_superuser:
        return True
    return UsuarioAutorizado.objects.filter(
        numero_usp=user.login,
        ativo=True
    ).exists()
```

## Como funciona

### Fluxo de autenticação

```
1. Usuário acessa página protegida
   ↓
2. LoginRequiredMixin redireciona para login
   ↓
3. Usuário autentica via Senha Única USP
   ↓
4. django-oauth-usp cria/atualiza UserModel (campo login = número USP)
   ↓
5. OAuthUSPAuthzBackend verifica se está na lista de autorizados
   ↓
6. Se não estiver na lista → login bloqueado
   ↓
7. Se estiver na lista → sessão criada
```

### Fluxo de verificação contínua

```
1. Usuário faz uma requisição
   ↓
2. OAuthUSPAuthzMiddleware verifica:
   - Se superusuário → segue normalmente
   - Se não-superusuário → verifica UsuarioAutorizado
   ↓
3. Se não estiver na lista ou inativo → logout + redirect para login
   ↓
4. Se estiver na lista e ativo → segue normalmente
```

## Estrutura do modelo

```python
class UsuarioAutorizado(models.Model):
    numero_usp = models.CharField(max_length=20, unique=True)
    ativo = models.BooleanField(default=True)
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
```

## Compatibilidade

- Django >= 4.2
- django-oauth-usp
- Python >= 3.10

## Licença

MIT
