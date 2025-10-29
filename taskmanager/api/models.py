from django.db import models
from django.contrib.auth.models import AbstractUser

class Projeto(models.Model):
    nome = models.CharField(max_length=50)
    descricao_projeto = models.CharField(max_length=100)

class Usuario(AbstractUser):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="membros")

class Tarefa(models.Model):
    titulo = models.CharField(max_length=30)
    descricao_tarefa = models.CharField(max_length=15)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="tarefas")
