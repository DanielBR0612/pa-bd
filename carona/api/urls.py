from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, PerfilUsuarioViewSet, VeiculoViewSet,
    CaronaViewSet, SolicitacaoViewSet, AvaliacaoViewSet, ChatViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfis', PerfilUsuarioViewSet, basename='perfil')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'caronas', CaronaViewSet, basename='carona')
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacao')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]