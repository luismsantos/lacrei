from django.urls import path
from .views import ProfissionalListCreateView, ProfissionalDetailView, ConsultaListCreateView, ConsultaDetailView

urlpatterns = [
    path('profissionais/', ProfissionalListCreateView.as_view(), name='profissionais-list'),
    path('profissionais/<int:id>/', ProfissionalDetailView.as_view(), name='profissionais-detail'),
    
    path('consultas/', ConsultaListCreateView.as_view(), name='consultas-list-create'),
    path('consultas/<int:id>/', ConsultaDetailView.as_view(), name='consultas-detail'),
]
