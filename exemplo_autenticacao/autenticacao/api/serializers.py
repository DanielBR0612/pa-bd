from rest_framework import serializers #type: ignore
from .models import MeuUsuario #type: ignore

class MeuUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeuUsuario
        fields = ['id', 'username', 'password', 'email']
        