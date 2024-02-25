# Generated by Django 4.2.4 on 2024-02-25 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_alocacao_agendamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alocacao',
            name='agendamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alocacao', to='api.agendamento'),
        ),
        migrations.AlterField(
            model_name='alocacao',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alocacao', to='api.paciente'),
        ),
    ]
