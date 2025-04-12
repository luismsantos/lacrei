from rest_framework import serializers
from .models import Profissional, Consulta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import date

#Validações
def validar_data_nascimento(value):
    """Valida se o profissional tem pelo menos 18 anos"""
    idade = relativedelta(date.today(), value).years
    if idade < 18:
        raise serializers.ValidationError("Profissional deve ter pelo menos 18 anos")

def validar_data_consulta(value):
    """Valida se a consulta não está no passado"""
    if value < timezone.now():
        raise serializers.ValidationError("Consulta não pode ser agendada no passado")


# Profissionais
class ProfissionalListSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField(
        format="%d/%m/%Y",
        input_formats=["%d/%m/%Y", "%Y-%m-%d"],
        validators=[validar_data_nascimento]
    )

    class Meta:
        model = Profissional
        fields = ['id', 'nome', 'nome_social', 'especialidade', 'data_nascimento']
        extra_kwargs = {
            'data_nascimento': {'validators': [validar_data_nascimento]}
        }

class ProfissionalDetailSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField(format="%d/%m/%Y")
    consultas = serializers.SerializerMethodField()

    class Meta:
        model = Profissional
        fields = ['id', 'nome', 'nome_social', 'especialidade', 'data_nascimento', 'consultas']

    def get_consultas(self, obj):
        return ConsultaSerializer(
            obj.consultas_profissional.all(),
            many=True,
            context=self.context
        ).data

# Consultas
class ConsultaSerializer(serializers.ModelSerializer):
    data_consulta = serializers.DateTimeField(
        format="%d/%m/%Y às %H:%M", 
        input_formats=["%d/%m/%Y às %H:%M", "%Y-%m-%dT%H:%M:%S"] 
    )

    class Meta:
        model = Consulta
        fields = ['id', 'data_consulta', 'nome_paciente', 'observacoes']
        extra_kwargs = {
            'data_consulta': {'validators': [validar_data_consulta]}
        }

class ConsultaListSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True)
    profissional_id = serializers.PrimaryKeyRelatedField(
        queryset=Profissional.objects.all(),
        source='profissional', 
        write_only=True
    )
    data_consulta = serializers.DateTimeField(
        format="%d/%m/%Y às %H:%M",
        input_formats=[
            "%d/%m/%Y às %H:%M",      
            "%Y-%m-%dT%H:%M:%S",          
            "%Y-%m-%dT%H:%M:%S.%fZ",      
            "%Y-%m-%dT%H:%M:%SZ"          
        ]
    )
    data_criacao = serializers.DateTimeField(format="%d/%m/%Y às %H:%M", read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 
            'profissional_id',
            'profissional_nome', 
            'nome_paciente', 
            'data_consulta',
            'observacoes',
            'data_criacao'
        ]
        extra_kwargs = {
            'data_consulta': {'validators': [validar_data_consulta]}
        }

class ConsultaDetailSerializer(serializers.ModelSerializer):
    profissional = serializers.SerializerMethodField()
    data_consulta = serializers.DateTimeField(format="%d/%m/%Y às %H:%M")
    data_criacao = serializers.DateTimeField(format="%d/%m/%Y às %H:%M")
    data_atualizacao = serializers.DateTimeField(format="%d/%m/%Y às %H:%M")

    class Meta:
        model = Consulta
        fields = [
            'id',
            'profissional',
            'nome_paciente',
            'data_consulta',
            'observacoes',
            'status',
            'data_criacao',
            'data_atualizacao'
        ]

    def get_profissional(self, obj):
        return {
            "id": obj.profissional.id,
            "nome": obj.profissional.nome,
            "nome_social": obj.profissional.nome_social,
            "especialidade": obj.profissional.especialidade,
            "data_nascimento": obj.profissional.data_nascimento.strftime("%d/%m/%Y"),
        }
