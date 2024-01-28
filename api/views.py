from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken

from .serializers import *

class MyRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['name'] = user.paciente.nome
        token['social_name'] = user.paciente.nome_social
        token['cpf'] = user.cpf

        return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
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
    def post(self, request, format=None):
        user = get_object_or_404(Cadastro, cpf=request.data["cpf"])

        correct_password = user.check_password(request.data["password"])
        if not correct_password:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tokens = MyRefreshToken().for_user(user)

        pass

from django.core.handlers.wsgi import WSGIRequest

class Signup(APIView):
    serializer_class = PacienteSerializer

    def post(self, request: WSGIRequest, format=None):
        print(" ")
        serializer = PacienteSerializer(data=request.data)

        if serializer.is_valid():
            paciente = serializer.save()

            Endereco.objects.create(uf=request.data["uf"], cidade=request.data["cidade"], bairro=request.data["bairro"], 
                                               complemento=request.data["complemento"], cep=request.data["cep"], paciente=paciente)

            paciente_serializer = PacienteSerializerReadOnly(paciente)

            return Response(paciente_serializer.data)

        return Response(serializer.errors)

def teste(request):
    # user = Paciente.objects.create(cpf="123.123.123-12", nome="Daniel", cns=1234)

    u = Paciente.objects.all()
    f = Fila.objects.all()
    c = Cadastro.objects.all()
    a = Alocacao.objects.all()
    ag = Agendamento.objects.all()

    print(u)
    print(" ")
    # print(f)
    print("Cadastro: ", c[1])
    # print(a)
    # print(ag)
    print(u[0].cadastro.all())


    return HttpResponse("Oi")