from django.db import models


class UsuarioAutorizado(models.Model):
    numero_usp = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número USP",
        help_text="Número USP do usuário autorizado a acessar o sistema."
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Desmarque para revogar o acesso sem excluir o registro."
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observação",
        help_text="Motivo da autorização ou qualquer outra anotação."
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuário Autorizado"
        verbose_name_plural = "Usuários Autorizados"
        ordering = ['numero_usp']

    def __str__(self):
        status = 'ativo' if self.ativo else 'inativo'
        return f"{self.numero_usp} ({status})"
