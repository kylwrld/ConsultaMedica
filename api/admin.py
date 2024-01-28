from django.contrib import admin
from .models import *

admin.site.register(Paciente)
admin.site.register(Endereco)
admin.site.register(Cadastro)
admin.site.register(Fila)
admin.site.register(Agendamento)
admin.site.register(Alocacao)

# Register your models here.
