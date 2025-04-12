from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from drf_yasg.utils import swagger_auto_schema  
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Profissional, Consulta
from .serializers import (
    ProfissionalDetailSerializer,
    ProfissionalListSerializer,
    ConsultaListSerializer,
    ConsultaDetailSerializer
)

# Profissional Endpoints
class ProfissionalListCreateView(generics.ListCreateAPIView):
    """
    Endpoint para listar todos os profissionais ou criar um novo.
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalListSerializer

    @swagger_auto_schema(
        responses={200: ProfissionalListSerializer(many=True)}
    )
    
    def get(self, request, *args, **kwargs):
        """
        Retorna a lista de todos os profissionais cadastrados.
        """
        return super().list(request, *args, **kwargs)


class ProfissionalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para buscar um profissional por ID, atualizar ou deletar.
    """
    queryset = Profissional.objects.all().prefetch_related('consultas_profissional')
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete'] 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfissionalDetailSerializer
        
        return ProfissionalListSerializer

    @swagger_auto_schema(
        request_body=ProfissionalListSerializer(partial=True),
        responses={
            200: ProfissionalListSerializer,
            400: "Dados inválidos",
            404: "Profissional não encontrado"
        }
    )
    
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

# Consulta endpoints
class ConsultaListCreateView(generics.ListCreateAPIView):
    """
    Endpoint para listar todas as consultas ou criar uma nova.
    """
    queryset = Consulta.objects.all().select_related('profissional')
    serializer_class = ConsultaListSerializer

    @swagger_auto_schema(
        responses={
            201: ConsultaListSerializer,
            400: "Dados inválidos"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConsultaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para buscar uma consulta por ID, atualizar ou deletar.
    """
    queryset = Consulta.objects.all().select_related('profissional')
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete'] 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConsultaDetailSerializer
        return ConsultaListSerializer

    @swagger_auto_schema(
        responses={
            200: ConsultaDetailSerializer,
            400: "Dados inválidos",
            404: "Consulta não encontrada"
        }
    )
    
    def patch(self, request, *args, **kwargs):
        """
        Atualiza parcialmente os dados de uma consulta específica.
        """
        return super().patch(request, *args, **kwargs)