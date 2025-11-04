from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(AbstractUser):
    
    TIPO_CHOICES = [
        ('MOTORISTA', 'Motorista'),
        ('PASSAGEIRO', 'Passageiro'),
        ('AMBOS', 'Ambos'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PASSAGEIRO')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class PerfilUsuario(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    verificado = models.BooleanField(default=False)
    nota_media = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
   
    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Veiculo(models.Model):
    
    motorista = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='veiculos',
        limit_choices_to={'tipo__in': ['MOTORISTA', 'AMBOS']}
    )
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    ano = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    placa = models.CharField(max_length=10, unique=True)
    num_lugares = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


class Carona(models.Model):
    
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('CHEIA', 'Cheia'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    motorista = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='caronas_oferecidas'
    )
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='caronas')
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    data_hora_saida = models.DateTimeField()
    vagas_disponiveis = models.IntegerField(validators=[MinValueValidator(0)])
    preco_por_pessoa = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    criado_em = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.origem} → {self.destino} - {self.data_hora_saida.strftime('%d/%m/%Y %H:%M')}"


class Solicitacao(models.Model):
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ACEITA', 'Aceita'),
        ('RECUSADA', 'Recusada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='solicitacoes')
    passageiro = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='solicitacoes_carona'
    )
    num_lugares = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.passageiro.username} - {self.get_status_display()}"


class Avaliacao(models.Model):
    
    TIPO_CHOICES = [
        ('MOTORISTA', 'Como Motorista'),
        ('PASSAGEIRO', 'Como Passageiro'),
    ]
    
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='avaliacoes_feitas'
    )
    avaliado = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='avaliacoes_recebidas'
    )
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.avaliador.username} avaliou {self.avaliado.username} - Nota: {self.nota}"


class Chat(models.Model):
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens')
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username}: {self.mensagem[:50]}"