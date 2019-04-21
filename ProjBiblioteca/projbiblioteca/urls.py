"""projbiblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from biblioteca.views import login, home, cadastrar, devolucao, emprestimo, novoLivro, novoAluno, consultarAlunos,\
    editarAluno, editarLivro, alunosBloqueados, confirmarPagamento, desbloquear, deslogar



urlpatterns = [
    path('admin/', admin.site.urls),
    path('biblioteca/',include('biblioteca.urls')),
    path('',login),
    path('deslogar/', deslogar),
    path('emprestimo/', emprestimo),
    path('novo-livro/', novoLivro),
    path('novo-aluno/', novoAluno),
    path('pesquisa/', home, name='pesquisa'),
    path('consultar-alunos/editar-aluno/(?P<value>\d+)', editarAluno, name='editaraluno'),
    path('editar-livro/(?P<value>\d+)', editarLivro, name='editarlivro'),
    path('quitar/(?P<value>\d+)',confirmarPagamento, name='quitar'),
    path('desbloqueio/(?P<aluno_id>\d+)', desbloquear, name='desbloquear'),
    path('devolucao/', devolucao, name='devolucao'),
    path('consultar-alunos/', consultarAlunos, name='pesquisa-alunos'),
    path('alunos-bloqueados/',alunosBloqueados, name='bloqueados'),
    path('envio/', cadastrar, name='envio')

]
