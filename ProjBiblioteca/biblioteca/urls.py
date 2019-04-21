from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verificar/', views.verificar, name='verificar'),
    path('confirmar/', views.confirmarDevolucao, name='confirmar-devolucao'),
    path('emprestimo-realizado/(?P<aluno_id>\d+)/$', views.salvar_emprestimo, name='realizado'),
    path('devolucao-completa/(?P<emprestimo_id>\d+)/$', views.desativar_emprestimo, name='desativar-emprestimo')
]