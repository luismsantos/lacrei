from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date, timedelta
from django.utils import timezone

from api.models import Profissional, Consulta


class LacreiAPITests(APITestCase):
    """Testes para a API Lacrei Saúde."""

    def setUp(self):
        """Configuração inicial para todos os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        # Criar um profissional para testes
        self.profissional = Profissional.objects.create(
            nome="Dra. Ana Silva",
            nome_social="Dr. André Silva",
            especialidade="Psicologia",
            data_nascimento=date(1985, 3, 15)
        )
        
        # Criar uma consulta para testes
        self.data_consulta = timezone.now() + timedelta(days=5)
        self.consulta = Consulta.objects.create(
            profissional=self.profissional,
            nome_paciente="João Oliveira",
            data_consulta=self.data_consulta,
            observacoes="Primeira consulta",
            status="AGENDADA"
        )
        
        self.profissionais_list_url = '/api/profissionais/'
        self.profissional_detail_url = f'/api/profissionais/{self.profissional.id}/'
        self.consultas_list_url = '/api/consultas/'
        self.consulta_detail_url = f'/api/consultas/{self.consulta.id}/'

    # Testes de Profissionais
    def test_listar_profissionais(self):
        """Teste para listar todos os profissionais."""
        response = self.client.get(self.profissionais_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_criar_profissional(self):
        """Teste para criar um novo profissional."""
        data = {
            "nome": "Dr. Carlos Santos",
            "especialidade": "Endocrinologia",
            "data_nascimento": "1978-07-22"
        }
        
        response = self.client.post(self.profissionais_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], "Dr. Carlos Santos")
    
    # Testes de Consultas
    def test_listar_consultas(self):
        """Teste para listar todas as consultas."""
        response = self.client.get(self.consultas_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_criar_consulta(self):
        """Teste para criar uma nova consulta."""
        future_date = timezone.now() + timedelta(days=7)
        formatted_date = future_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
        data = {
        "profissional_id": self.profissional.id,
        "nome_paciente": "Maria Souza",
        "data_consulta": formatted_date,  
        "observacoes": "Consulta de retorno"
        }
    
        response = self.client.post(self.consultas_list_url, data, format='json')
    
        print(f"Response status: {response.status_code}, Response data: {response.data}")
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome_paciente'], "Maria Souza")