from django.urls import path
from . import views
 
app_name='os_ti'
urlpatterns = [
    path('os/reset/conclusao/123654/', views.mudadados, name='mudados'),
    path('os/alterar_equipes/123456/', views.alterar_equipes, name='alterar_equipes'),

    path('', views.os_index, name='os_index'),
    path('finalizados/', views.os_finalizados, name='os_finalizados'),
    path('painel/', views.os_painel, name='os_painel'),
    path('os/', views.add_os, name='add_os'),
    path('os/contar-os/', views.contagem_os, name='contagem_os'),
    path('os/salvar-contagem/', views.salvar_contagem_os, name='salvar_contagem_os'),

    path('os/painel/<id>/', views.detalhes_os, name='detalhes_os'),
    path('os/painel/<id>/pontos', views.pontos_os, name='pontos_os'),
    path('imprimir/', views.os_index, name='imprimir_nada'),
    path('imprimir/<ids>/', views.imprimir_varias_os, name='imprimir_varias'),
    path('os/painel/<id>/imprimir/', views.imprimir_os, name='imprimir'),
    path('os/painel/<id>/alterar_status/<opcao>', views.change_status_os, name='change_status_os'),
    path('os/painel/<id>/alterar_prioridade/<opcao>', views.change_prioridade_os, name='change_prioridade_os'),
    path('os/painel/<id>/atender', views.atender_os, name='atender_os'),

    path('os/kpi', views.graficos, name='kpi'),
    path('os/kpi/ver-mais/<tipo>/<subtipo>/', views.graficos_ver_mais, name='kpi_ver_mais'),
    path('funcionario', views.funcionarios_listar, name='funcionarios'),
    path('funcionario/cadastrar/', views.funcionario_cadastrar, name='cadastrar funcionario'),
    path('funcionario/editar/<id>/', views.funcionario_editar, name='editar funcionario'),
    path('funcionario/deletar/<id>/', views.funcionario_deletar, name='deletar funcionario'),

    path('os/painel/<id>/equipe/', views.atribuir_equipe, name='atribuir equipe')
]