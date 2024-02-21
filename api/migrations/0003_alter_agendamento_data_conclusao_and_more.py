# Generated by Django 5.0.1 on 2024-01-31 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_descricacao_agendamento_descricao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='data_conclusao',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='data_prevista',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='preferencia',
            field=models.CharField(blank=True, choices=[('SEM PREFERÊNCIA', 'Sem preferência'), ('DEFICIENTE', 'Deficiente'), ('IDOSO', 'Idoso'), ('GESTANTE', 'Gestante'), ('LACTANTE', 'Lactante'), ('OBESO', 'Obeso'), ('CRIANÇA DE COLO', 'Criança de colo')], max_length=25),
        ),
    ]
