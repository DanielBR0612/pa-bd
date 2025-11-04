from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat
from .serializers import (
    UsuarioSerializer, PerfilUsuarioSerializer, VeiculoSerializer,
    CaronaSerializer, SolicitacaoSerializer, AvaliacaoSerializer, ChatSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['motorista', 'ativo']
    search_fields = ['modelo', 'marca', 'placa']


class CaronaViewSet(viewsets.ModelViewSet):
    queryset = Carona.objects.all()
    serializer_class = CaronaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['motorista', 'status', 'origem', 'destino']
    search_fields = ['origem', 'destino']
    ordering_fields = ['data_hora_saida', 'preco_por_pessoa']
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Retorna apenas caronas disponíveis"""
        caronas = self.queryset.filter(status='DISPONIVEL', vagas_disponiveis__gt=0)
        serializer = self.get_serializer(caronas, many=True)
        return Response(serializer.data)


class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'passageiro', 'status']
    
    @action(detail=True, methods=['post'])
    def aceitar(self, request, pk=None):
        """Aceitar uma solicitação"""
        solicitacao = self.get_object()
        solicitacao.status = 'ACEITA'
        solicitacao.save()
        return Response({'status': 'Solicitação aceita'})
    
    @action(detail=True, methods=['post'])
    def recusar(self, request, pk=None):
        """Recusar uma solicitação"""
        solicitacao = self.get_object()
        solicitacao.status = 'RECUSADA'
        solicitacao.save()
        return Response({'status': 'Solicitação recusada'})


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'avaliador', 'avaliado', 'tipo']


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'usuario']