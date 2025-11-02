from django.db import models
from django.contrib.auth.models import AbstractUser

class Projeto(models.Model):
    nome = models.CharField(max_length=50)
    descricao_projeto = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.nome} - {self.descricao_projeto}'

class Usuario(AbstractUser):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="membros", null=True)
    
    def __str__(self):
        return f'{self.username} - {self.projeto}'

class Tarefa(models.Model):
    titulo = models.CharField(max_length=30)
    descricao_tarefa = models.CharField(max_length=100)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="tarefas")
    
    def __str__(self):
        return f'{self.titulo} - {self.descricao_tarefa} - {self.projeto}'
