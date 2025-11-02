from rest_framework import serializers 
from .models import Usuario, Tarefa, Projeto 

class UsuarioSerializer(serializers.ModelSerializer):
    projeto = serializers.StringRelatedField(read_only=True) 

    projeto_id = serializers.PrimaryKeyRelatedField(
        queryset=Projeto.objects.all(), 
        source='projeto',               
        write_only=True,               
        required=False,                 
        allow_null=True                
    )
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'email',
            'projeto',  
            'projeto_id',  
            'password'     
        ]
        
        read_only_fields = ['id', 'projeto']
        
class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ['id', 'titulo', 'descricao_tarefa', 'projeto']
        
class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'nome', 'descricao_projeto']
        