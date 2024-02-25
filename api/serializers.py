from rest_framework import serializers
from .models import *
from django.utils import timezone

class FilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fila
        fields = ['nome_fila', 'especialidade']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['uf', 'cidade', 'bairro', 'complemento', 'cep']

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['cpf', 'nome', 'nome_social', 'cns']

class PacienteSerializerReadOnly(serializers.ModelSerializer):
    endereco = EnderecoSerializer(read_only=True, many=True)

    class Meta:
        model = Paciente
        fields = ['cpf', 'nome', 'nome_social', 'cns', 'endereco']

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = ['cpf', 'password']

class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = ['especialidade', 'descricao', 'preferencia', 'data_prevista', 'data_conclusao']