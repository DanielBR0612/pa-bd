from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo', 'is_staff']
    list_filter = ['tipo', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('tipo',)}),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefone', 'verificado', 'nota_media']
    list_filter = ['verificado']
    search_fields = ['usuario__username', 'telefone']

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'marca', 'modelo', 'motorista', 'ativo']
    list_filter = ['ativo', 'marca']
    search_fields = ['placa', 'modelo', 'motorista__username']

@admin.register(Carona)
class CaronaAdmin(admin.ModelAdmin):
    list_display = ['origem', 'destino', 'motorista', 'data_hora_saida', 'status', 'vagas_disponiveis']
    list_filter = ['status', 'data_hora_saida']
    search_fields = ['origem', 'destino', 'motorista__username']
    date_hierarchy = 'data_hora_saida'

@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ['carona', 'passageiro', 'num_lugares', 'status', 'data_solicitacao']
    list_filter = ['status', 'data_solicitacao']
    search_fields = ['passageiro__username']

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['avaliador', 'avaliado', 'nota', 'tipo', 'criado_em']
    list_filter = ['nota', 'tipo']
    search_fields = ['avaliador__username', 'avaliado__username']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['carona', 'usuario', 'mensagem', 'data_hora']
    list_filter = ['data_hora']
    search_fields = ['usuario__username', 'mensagem']
    date_hierarchy = 'data_hora'