from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    ano = models.DateField()
    genero = models.CharField(max_length=25)

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    dt_nascimento = models.DateField()
    nacionalidade = models.CharField(max_length=20)
    
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dt_cadastro = models.DateField(auto_now_add=True)

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, related_name='Emprestimos')
    usuario = models.ForeignKey(Usuario, related_name='Emprestimo')
    dt_emprestimo = models.DateField(auto_now_add=True)
    
class Reserva(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='Reservas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='Reservas')
    dt_reserva = models.DateField()

class Multa(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='Multas')
    valor = models.FloatField(default=0)
    dt_pagamento = models.DateField()

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=15)
    descricao = models.TextField()

class Editora(models.Model):
    nome_editora = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100)
