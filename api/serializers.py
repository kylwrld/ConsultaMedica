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

class EnderecoSerializerUpdate(serializers.ModelSerializer):
    uf = serializers.CharField(max_length=2, required=False)
    cidade = serializers.CharField(max_length=30, required=False)
    bairro = serializers.CharField(max_length=30, required=False)
    complemento = serializers.CharField(max_length=30, required=False)
    cep = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = Endereco
        fields = ['uf', 'cidade', 'bairro', 'complemento', 'cep']

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)

        super(EnderecoSerializerUpdate, self).update(instance, validated_data)
        return instance

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['cpf', 'nome', 'nome_social', 'cns']

class PacienteSerializerReadOnly(serializers.ModelSerializer):
    endereco = EnderecoSerializer(read_only=True)

    class Meta:
        model = Paciente
        fields = ['cpf', 'nome', 'nome_social', 'cns', 'endereco']

class PacienteSerializerUpdate(serializers.ModelSerializer):
    nome = serializers.CharField(max_length=60, required=False)
    nome_social = serializers.CharField(max_length=60, required=False)
    cns = serializers.IntegerField(required=False)
    
    class Meta:
        model = Paciente
        fields = ['nome', 'nome_social', 'cns']

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = ['cpf', 'password']

class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = ['especialidade', 'descricao', 'preferencia', 'data_prevista', 'data_conclusao']