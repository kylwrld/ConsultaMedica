from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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

from .serializers import *

class MyToken(Token):
    def for_user(cls, user):
        # token = super().for_user(user)
        token = cls()
        token['name'] = user.paciente.nome
        token['social_name'] = user.paciente.nome_social
        token['cpf'] = user.cpf

        if api_settings.CHECK_REVOKE_TOKEN:
            token[api_settings.REVOKE_TOKEN_CLAIM] = get_md5_hash_password(
                user.password
            )

        return token

class MyRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        # token = super().for_user(user)
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

            Endereco.objects.create(uf=request.data["uf"], cidade=request.data["cidade"], bairro=request.data["bairro"], 
                                               complemento=request.data["complemento"], cep=request.data["cep"], paciente=paciente)

            cadastro = Cadastro.objects.create(cpf=paciente.cpf, paciente=paciente)
            cadastro.set_password(request.data["password"])
            cadastro.save()

            paciente_serializer = PacienteSerializerReadOnly(paciente)

            refresh = MyRefreshToken.for_user(cadastro)
            
            data = {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user": paciente_serializer.data,
            }
            
            return Response(data=data, status=status.HTTP_201_CREATED)

            # return Response(paciente_serializer.data)

        return Response(serializer.errors)

def teste(request):

    u = Paciente.objects.all()
    f = Fila.objects.all()
    c = Cadastro.objects.all()
    a = Alocacao.objects.all()
    ag = Agendamento.objects.all()

    print(u)
    print(" ")
    # print(f)
    print("Cadastro: ", c[0])
    # print(a)
    # print(ag)
    print(u[0].cadastro.all())


    return HttpResponse("Oi")