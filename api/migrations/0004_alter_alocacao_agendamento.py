# Generated by Django 5.0.1 on 2024-02-04 23:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_agendamento_data_conclusao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alocacao',
            name='agendamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agendamento', to='api.agendamento'),
        ),
    ]