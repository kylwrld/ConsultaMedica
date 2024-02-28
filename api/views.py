from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import get_md5_hash_password
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from .serializers import *

from time import perf_counter 

class MyRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = cls()
        token['name'] = user.paciente.nome
        token['social_name'] = user.paciente.nome_social
        token['cpf'] = user.cpf

        if api_settings.CHECK_REVOKE_TOKEN:
            token[api_settings.REVOKE_TOKEN_CLAIM] = get_md5_hash_password(
                user.password
            )

        return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = MyRefreshToken

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.paciente.nome
        token['social_name'] = user.paciente.nome_social
        token['cpf'] = user.cpf

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Login(APIView):
    # parameters:
    #               cpf, password

    def post(self, request, format=None):
        user = get_object_or_404(Cadastro, cpf=request.data["cpf"])

        correct_password = user.check_password(request.data["password"])
        if not correct_password:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tokens = MyRefreshToken().for_user(user)

        data = {
            "refresh": str(tokens),
            "access": str(tokens.access_token),
        }


        return Response({"detail":"approved", "token":data}, status=status.HTTP_201_CREATED)

from django.core.handlers.wsgi import WSGIRequest

class Signup(APIView):
    serializer_class = PacienteSerializer

    # parameters: 
    #               cpf, password, nome, nome_social, cns
    #               uf, cidade, bairro, complemento, cep

    def post(self, request: WSGIRequest, format=None):
        serializer = PacienteSerializer(data=request.data)

        if serializer.is_valid():
            paciente = serializer.save()

            endereco_serializer = EnderecoSerializer(data=request.data)
            if endereco_serializer.is_valid():
                endereco_serializer.save(paciente=paciente)

            # Endereco.objects.create(uf=request.data["uf"], cidade=request.data["cidade"], bairro=request.data["bairro"], 
                                            #    complemento=request.data["complemento"], cep=request.data["cep"], paciente=paciente)


            cadastro = Cadastro.objects.create(cpf=paciente.cpf, paciente=paciente)
            cadastro.set_password(request.data["password"])
            cadastro.save()

            paciente_serializer = PacienteSerializerReadOnly(paciente)

            refresh = MyRefreshToken().for_user(cadastro)
            
            data = {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user": paciente_serializer.data,
            }
            
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

class FilaEndpoint(APIView):
    def post(self, request, format=None):
        try:
            Fila.objects.get(nome_fila=request.data["nome_fila"], especialidade=request.data["especialidade"])
            return Response({"detail":"Fila já existe."}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            fila_serializer = FilaSerializer(data=request.data)

            if fila_serializer.is_valid():
                fila_serializer.save()

                return Response({"detail":"Fila criada com sucesso.", "fila":fila_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(fila_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # parameters:
    #               nome_fila, especialidade
    def delete(self, request, format=None):
        try:
            fila = Fila.objects.get(nome_fila=request.data["nome_fila"], especialidade=request.data["especialidade"])
            fila.delete()
        except ObjectDoesNotExist:
            return Response({"detail":"Fila não existe."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail":"Fila deletada com sucesso."}, status=status.HTTP_200_OK)

    # parameters:
    #               novo_medico, nova_especialidade
    def put(self, request, format=None):
        try:
            fila = Fila.objects.get(nome_fila=request.data["nome_fila"], especialidade=request.data["especialidade"])
        except ObjectDoesNotExist:
            return Response({"detail":"Fila não existe."}, status=status.HTTP_404_NOT_FOUND)

        data = {}

        if "novo_medico" in request.data:
            data["nome_fila"] = request.data["novo_medico"]
        if "nova_especialidade" in request.data:
            data["especialidade"] = request.data["nova_especialidade"]

        fila_serializer = FilaSerializer(fila, data=data)

        if fila_serializer.is_valid():
            fila_serializer.save()
            return Response({"detail":"Fila atualizada com sucesso."}, status=status.HTTP_201_CREATED)
        return Response(fila_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultaUser(APIView):
    
    permission_classes = [IsAuthenticated]

    # parameters: 
    #               especialidade, descricao
    #               preferencia, nome_fila,
    #               data_prevista, data_conclusao
    def post(self, request: WSGIRequest, format=None):

        agendamento_serializer = AgendamentoSerializer(data=request.data)

        if agendamento_serializer.is_valid():
            paciente = Paciente.objects.get(cpf=request.user.cpf)

            if len(Agendamento.objects.filter(especialidade=request.data["especialidade"], paciente=paciente)) >= 1:
                return Response({"detail":"Consulta com médico já criada."}, status=status.HTTP_400_BAD_REQUEST)

            fila, _ = Fila.objects.get_or_create(nome_fila=request.data["nome_fila"], especialidade=request.data["especialidade"])
            paciente.filas.add(fila)
            paciente.save()
            agendamento = agendamento_serializer.save(paciente=paciente)

            print("\nAGENDAMENTO: ", agendamento, "\n")
            alocacao = Alocacao.objects.filter(paciente=paciente)
            alocacao = alocacao[len(alocacao)-1]
            alocacao.save(agendamento=agendamento)

            return Response(agendamento_serializer.data)
        return Response(agendamento_serializer.errors)
    
    def delete(self, request, format=None):
        paciente = request.user.paciente
        agendamento = get_object_or_404(Agendamento, paciente=paciente, especialidade=request.data["especialidade"])

        fila = get_object_or_404(Fila, nome_fila=request.data["nome_fila"], especialidade=request.data["especialidade"])

        agendamento.delete()
        paciente.filas.remove(fila)

        return Response(data={"detail":"Item deletado com sucesso"}, status=status.HTTP_200_OK)
    
    # parameters:
    #               nova_especialidade + AgendamentoModelFields
    def put(self, request, format=None):
        if self.check_queue(request.user.paciente, request.data["nova_especialidade"], request.data["novo_medico"]):
            return Response({"detail":"Usuário já cadastrado na fila."}) 

        try:
            agendamento = Agendamento.objects.get(paciente=request.user.paciente, especialidade=request.data["especialidade"])
        except ObjectDoesNotExist:
            return Response({"detail":"Fila não existe."}, status=status.HTTP_404_NOT_FOUND)

        if "nova_especialidade" in request.data:
            try:
                fila = Fila.objects.get(nome_fila=request.data["novo_medico"], especialidade=request.data["nova_especialidade"])
            except ObjectDoesNotExist:
                return Response({"detail":"Fila não existe."}, status=status.HTTP_404_NOT_FOUND)

            request.data["especialidade"] = request.data["nova_especialidade"]

        agendamento_serializer = AgendamentoSerializer(agendamento, data=request.data)

        if agendamento_serializer.is_valid():
            agendamento = agendamento_serializer.save()
            alocacao = agendamento.alocacao
            alocacao.fila = fila
            alocacao.save()

            return Response(data=agendamento_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=agendamento_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def check_queue(client, new_spec, new_doc):
        try:
            agendamento_update = Agendamento.objects.get(paciente=client, especialidade=new_spec)
            if agendamento_update.alocacao.fila.nome_fila == new_doc:
                return True
        except:
            return False

class User(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, format=None):
        paciente = request.user.paciente
        paciente.delete()

        return Response({"detail":"Paciente deletado com sucesso."}, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        paciente = request.user.paciente
        
        if "cpf" in request.data:
            return Response({"detail":"Não pode mudar o CPF."}, status=status.HTTP_400_BAD_REQUEST)

        paciente_serializer = PacienteSerializerUpdate(paciente, data=request.data)

        if paciente_serializer.is_valid():
            paciente = paciente_serializer.save()
            
            print(paciente.endereco)

            endereco_serializer = EnderecoSerializerUpdate(paciente.endereco, data=request.data)
            if endereco_serializer.is_valid():
                print("AAAAAAAAAAAAAAA!@#!@!@#DAS-")
                endereco_serializer.save()

                return Response({"detail":"Todos os dados foram atualizados. 1"}, status=status.HTTP_201_CREATED)

            return Response({"detail":"Todos os dados foram atualizados. 2"}, status=status.HTTP_201_CREATED)
        return Response(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)