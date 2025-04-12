# Generated by Django 5.2 on 2025-04-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='paciente',
        ),
        migrations.AddField(
            model_name='consulta',
            name='nome_paciente',
            field=models.CharField(default='Paci', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consulta',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profissional',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Paciente',
        ),
    ]
