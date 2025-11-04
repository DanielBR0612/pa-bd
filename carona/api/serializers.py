from rest_framework import serializers
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'foto', 'biografia', 'verificado', 'nota_media']


class UsuarioSerializer(serializers.ModelSerializer):
    perfil = PerfilUsuarioSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo', 'perfil']
        read_only_fields = ['id']


class VeiculoSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.username', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = [
            'id', 'motorista', 'motorista_nome', 'modelo', 'marca', 
            'cor', 'ano', 'placa', 'num_lugares', 'ativo'
        ]
        read_only_fields = ['id']


class CaronaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.username', read_only=True)
    veiculo_info = serializers.CharField(source='veiculo.__str__', read_only=True)
    
    class Meta:
        model = Carona
        fields = [
            'id', 'motorista', 'motorista_nome', 'veiculo', 'veiculo_info',
            'origem', 'destino', 'data_hora_saida', 'vagas_disponiveis',
            'preco_por_pessoa', 'observacoes', 'status', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class SolicitacaoSerializer(serializers.ModelSerializer):
    passageiro_nome = serializers.CharField(source='passageiro.username', read_only=True)
    carona_info = serializers.CharField(source='carona.__str__', read_only=True)
    
    class Meta:
        model = Solicitacao
        fields = [
            'id', 'carona', 'carona_info', 'passageiro', 'passageiro_nome',
            'num_lugares', 'status', 'data_solicitacao'
        ]
        read_only_fields = ['id', 'data_solicitacao']


class AvaliacaoSerializer(serializers.ModelSerializer):
    avaliador_nome = serializers.CharField(source='avaliador.username', read_only=True)
    avaliado_nome = serializers.CharField(source='avaliado.username', read_only=True)
    
    class Meta:
        model = Avaliacao
        fields = [
            'id', 'carona', 'avaliador', 'avaliador_nome', 
            'avaliado', 'avaliado_nome', 'nota', 'comentario', 
            'tipo', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class ChatSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'carona', 'usuario', 'usuario_nome', 'mensagem', 'data_hora']
        read_only_fields = ['id', 'data_hora']