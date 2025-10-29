from rest_framework import serializers
from .models import Projeto, Tarefa, Usuario

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'nome', 'descricao', 'data_inicio', 'data_fim']

class TarefaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tarefa
        fields = ['id', 'titulo', 'descricao', 'data_criacao', 'data_conclusao', 'projeto']
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'projeto']

        def create(self, validated_data);
            password = validated_data.pop('password')
            user = Usuario.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user

#class based views
from rest_framework import viewsets, status
from rest_framework.permission_classes import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.viewas import APIView
from .models import Projeto, Tarefa, Usuario  from rest_framework import serializers
from .models import Projeto, Tarefa, Usuario


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ["id", "nome", "descricao_projeto"]


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ["id", "titulo", "descricao_tarefa", "projeto"]


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email"]


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario.objects.create_user(**validated_data) 
        user.set_password(password)
        user.save()
        return user
