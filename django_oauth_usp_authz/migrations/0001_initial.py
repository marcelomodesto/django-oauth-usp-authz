from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioAutorizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_usp', models.CharField(help_text='Número USP do usuário autorizado a acessar o sistema.', max_length=20, unique=True, verbose_name='Número USP')),
                ('ativo', models.BooleanField(default=True, help_text='Desmarque para revogar o acesso sem excluir o registro.', verbose_name='Ativo')),
                ('observacao', models.TextField(blank=True, help_text='Motivo da autorização ou qualquer outra anotação.', null=True, verbose_name='Observação')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Usuário Autorizado',
                'verbose_name_plural': 'Usuários Autorizados',
                'ordering': ['numero_usp'],
            },
        ),
    ]
