from django.contrib import admin
from django_oauth_usp_authz.models import UsuarioAutorizado


@admin.register(UsuarioAutorizado)
class UsuarioAutorizadoAdmin(admin.ModelAdmin):
    list_display = ('numero_usp', 'ativo', 'observacao', 'criado_em', 'atualizado_em')
    list_filter = ('ativo',)
    search_fields = ('numero_usp', 'observacao')
    list_editable = ('ativo',)
    readonly_fields = ('criado_em', 'atualizado_em')
