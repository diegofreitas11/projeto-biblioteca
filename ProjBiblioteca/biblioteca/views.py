from django.shortcuts import render
from django.db.models import Q
from .models import Aluno, Livro, Emprestimo, Usuario
import datetime
import pytz
import locale
import json

# Create your views here.


def login(request):
    usuarios = Usuario.objects.all()
    html = 'biblioteca/login.html'
    variaveis = dict()
    variaveis["linhas"] = carrega_livros(None)

    for usuario in usuarios:
        if usuario.logado:
            html = 'biblioteca/index.html'

    return render(request, html, variaveis)


def deslogar(request):
    usuarios = Usuario.objects.all()

    for usuario in usuarios:
        if usuario.logado:
            usuario.logado = False
            usuario.save()

    return render(request, 'biblioteca/login.html')


def home(request):
    usuarios = Usuario.objects.all()
    html = ""
    aviso = ""
    variaveis = dict()
    if "txt_pesquisa" in request.POST:
        variaveis["linhas"] = carrega_livros(request.POST["txt_pesquisa"])
        html = 'biblioteca/index.html'
        return render(request, html, variaveis)
    else:
        variaveis["linhas"] = carrega_livros(None)

    for usuario in usuarios:
        if request.POST["txt_usuario"] == usuario.login and request.POST["txt_senha"] == usuario.senha:
            html = 'biblioteca/index.html'
            usuario.logado = True
            usuario.save()

    if html == '':
        html = 'biblioteca/login.html'
        aviso = 'Usuário e/ou senha incorretos!'

    variaveis["aviso"] = aviso

    return render(request, html, variaveis)


def novoAluno(request):
    return render(request, 'biblioteca/cadastro_aluno.html')


def editarAluno(request, value):
    aluno = Aluno.objects.get(matricula=value)

    campos = {}
    variaveis = dict()

    campos[0] = aluno.matricula
    campos[1] = aluno.nome
    campos[2] = aluno.rg
    campos[3] = aluno.periodo
    campos[4] = aluno.ano
    campos[5] = aluno.senha
    variaveis["campos"] = campos

    return render(request,'biblioteca/cadastro_aluno.html', variaveis)


def novoLivro(request):
    return render(request, 'biblioteca/cadastro_livro.html')


def editarLivro(request, value):
    livro = Livro.objects.get(id=value)

    campos = {}
    variaveis = dict()
    if livro.descricao:
        campos[0] = livro.descricao
    campos[1] = livro.nome
    campos[2] = livro.genero
    campos[3] = livro.autor
    campos[4] = livro.ano
    campos[5] = livro.quantidade
    campos[6] = livro.editora
    campos[7] = livro.id
    variaveis["campos"] = campos

    return render(request, 'biblioteca/cadastro_livro.html', variaveis)


def consultarAlunos(request):
    variaveis = {}

    if 'txt_pesquisa' in request.POST:
        filtro = request.POST['txt_pesquisa']
    else:
        filtro = None

    variaveis["linhas"] = carrega_alunos(filtro, False)
    return render(request, 'biblioteca/consultar_alunos.html', variaveis)


def cadastrar(request):
    variaveis = {}

    if "txt_rg" in request.POST:
        if request.POST["btn_cadastrar"] == "insert":
            aluno = Aluno()
        else:
            aluno = Aluno.objects.get(matricula=request.POST["txt_matricula"])

        html = 'biblioteca/cadastro_aluno.html'
        if request.POST["txt_nome"] != "" and request.POST["txt_rg"] != "" and request.POST["txt_matricula"] != "" \
        and request.POST["txt_periodo"] != "" and request.POST["txt_ano"] != "" and request.POST["txt_senha"] != "":
            aluno.nome = request.POST["txt_nome"]
            aluno.rg = request.POST["txt_rg"]
            aluno.matricula = request.POST["txt_matricula"]
            aluno.periodo = request.POST["txt_periodo"]
            aluno.ano = request.POST["txt_ano"]
            aluno.senha = request.POST["txt_senha"]
            aluno.save()
            variaveis["mensagem"] = "Aluno cadastrado com sucesso"
        else:
            variaveis["mensagem"] = "Preencha todos os campos!"
    else:
        if request.POST["btn_cadastrar"] == "insert":
            livro = Livro()
        else:
            livro = Livro.objects.get(id=request.POST["txt_id"])

        html = 'biblioteca/cadastro_livro.html'
        if request.POST["txt_nome"] != "" and request.POST["txt_genero"] != "" and request.POST["txt_autor"] != "" \
        and request.POST["txt_editora"] != "" and request.POST["txt_ano"] != "" and request.POST["txt_descr"] != "" \
        and request.POST["txt_qtd"] != "":
            livro.nome = request.POST["txt_nome"]
            livro.genero = request.POST["txt_genero"]
            livro.autor = request.POST["txt_autor"]
            livro.editora = request.POST["txt_editora"]
            livro.ano = request.POST["txt_ano"]
            livro.descricao = request.POST["txt_descr"]
            livro.quantidade = request.POST["txt_qtd"]
            livro.save()
            variaveis["mensagem"] = "Livro cadastrado com sucesso!"

        else:
            variaveis["mensagem"] = "Preencha todos os campos!"

    return render(request,html, variaveis)


def emprestimo(request):
    variaveis = dict()

    variaveis["inicio"] = 1
    variaveis["valido"] = 0
    variaveis["matricula"] = "xxx"
    variaveis["id"] = 0

    return render(request,'biblioteca/registrar_emprestimo.html', variaveis)


def verificar(request):
    alunos = Aluno.objects.all()
    valido = 0
    variaveis = {}
    bloqueado = False

    if "txt_procurar_aluno" in request.POST:
        filtro = None
        aluno_id = request.POST["txt_procurar_aluno"]
        for aluno in alunos:
            if aluno_id == aluno.matricula:
                if not aluno.status == "bloqueado":
                    valido = 1
                    variaveis["nome"] = aluno.nome
                else:
                    bloqueado = True
                    # variaveis["id"] = aluno.matricula
            pass

        if bloqueado:
            variaveis["aviso"] = "Aluno bloqueado"
        else:
            variaveis["aviso"] = "Matrícula não encontrada."

        emprestimos = Emprestimo.objects.filter(status="ativo")

        for emprestimo in emprestimos:
            if emprestimo.aluno.matricula == aluno_id:
                valido = 0
                variaveis["aviso"] = "Usuário já tem livro em empréstimo."

        variaveis["inicio"] = 0
        variaveis["valido"] = valido
    else:
        variaveis["inicio"] = 0
        variaveis["valido"] = 1
        aluno_id = request.POST["pesquisar"]
        aluno = Aluno.objects.get(matricula=aluno_id)
        variaveis["nome"] = aluno.nome
        filtro = request.POST["txt_pesquisa"]

    variaveis['linhas'] = carrega_livros(filtro)
    variaveis["matricula"] = aluno_id

    return render(request, 'biblioteca/registrar_emprestimo.html', variaveis)


def salvar_emprestimo(request, aluno_id):
    variaveis = {}
    emprestimo = Emprestimo()
    livro = Livro.objects.get(id=request.POST["selecionar-livro"])
    livro.quantidade = livro.quantidade - 1
    emprestimo.livro = livro
    livro.save()
    aluno = Aluno.objects.get(matricula=aluno_id)
    emprestimo.aluno = aluno
    emprestimo.data = datetime.datetime.today() + datetime.timedelta(days=10)
    emprestimo.status = "ativo"
    emprestimo.save()

    variaveis["inicio"] = 1
    variaveis["aviso"] = "Empréstimo salvo com sucesso!"
    variaveis["id"] = 0
    variaveis["matricula"] = "0"

    return render(request, 'biblioteca/registrar_emprestimo.html', variaveis)


def desativar_emprestimo(request, emprestimo_id):
    variaveis = {}
    bloqueio = False
    if request.POST["op"] == "sim":
        utc = pytz.utc
        data_atual = utc.localize(datetime.datetime.today())
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        if emprestimo.data < data_atual:
            bloqueio = True

        emprestimo.status = "desativado"
        livro = Livro.objects.get(id=emprestimo.livro.id)
        livro.quantidade = livro.quantidade + 1
        livro.save()

        if "pagamento" not in request.POST:
            if bloqueio:
                aluno = Aluno.objects.get(matricula=emprestimo.aluno.matricula)
                aluno.status = "bloqueado"
                atraso = data_atual - emprestimo.data
                aluno.valor_debito = float(atraso.days)
                aluno.save()

        emprestimo.save()
        variaveis["aviso"] = "devolução registrada com sucesso."

    variaveis['linhas'] = carrega_emprestimos(None)

    return render(request,'biblioteca/registrar_devolucao.html', variaveis)


def alunosBloqueados(request):
    variaveis = {}

    if "txt_pesquisa" in request.POST:
        variaveis["linhas"] = carrega_alunos(request.POST["txt_pesquisa"], True)
    else:
        variaveis["linhas"] = carrega_alunos(None, True)

    return render(request, 'biblioteca/alunos_bloqueados.html',variaveis)


def confirmarPagamento(request, value):
    variaveis = {}
    locale.setlocale(locale.LC_ALL, '')
    aluno = Aluno.objects.get(matricula=value)
    variaveis["nome"] = aluno.nome
    variaveis["valor"] = locale.currency(aluno.valor_debito)
    variaveis["id"] = aluno.matricula

    return render(request, 'biblioteca/confirmar_pagamento.html', variaveis)


def desbloquear(request, aluno_id):
    variaveis = {}

    if request.POST["op"] == "sim":
        aluno = Aluno.objects.get(matricula=aluno_id)
        aluno.valor_debito = 0
        aluno.status = "ativo"
        aluno.save()

    variaveis["linhas"] = carrega_alunos(None, True)

    return render(request,'biblioteca/alunos_bloqueados.html', variaveis)


def devolucao(request):
    variaveis = {}

    if "txt_pesquisa" in request.POST:
        filtro = request.POST["txt_pesquisa"]
    else:
        filtro = None

    variaveis['linhas'] = carrega_emprestimos(filtro)

    return render(request, 'biblioteca/registrar_devolucao.html', variaveis)


def confirmarDevolucao(request):
    variaveis = {}
    locale.setlocale(locale.LC_ALL,'')
    emprestimos = Emprestimo.objects.filter(id=request.POST["op_devolucao"])
    utc = pytz.utc
    data_atual = utc.localize(datetime.datetime.today())

    for emprestimo in emprestimos:

        variaveis["livro"] = emprestimo.livro.nome
        variaveis["aluno"] = emprestimo.aluno.nome

        if emprestimo.data < data_atual:
            atraso = data_atual - emprestimo.data
            variaveis["multa"] = locale.currency(atraso.days)

    variaveis["id"] = request.POST["op_devolucao"]

    return render(request, 'biblioteca/confirmar_devolucao.html', variaveis)


def carrega_livros(filtro):
    linhas = []
    if filtro:
        livros = Livro.objects.filter(nome__contains=filtro)
    else:
        livros = Livro.objects.filter(quantidade__gt=0)
    dic = {}

    for livro in livros:
        dic['id'] = livro.id
        dic['nome'] = livro.nome
        dic['genero'] = livro.genero
        dic['autor'] = livro.autor
        dic['ano'] = livro.ano
        dic['quantidade'] = livro.quantidade
        linhas.append(dic.copy())
        dic.clear()

    return linhas


def carrega_emprestimos(filtro):
    linhas = []
    dic = {}

    if filtro:
        emprestimos = Emprestimo.objects.filter(
            status="ativo"
        ).filter(
            Q(livro__nome__contains=filtro) | Q(aluno__nome__contains=filtro)
        )
    else:
        emprestimos = Emprestimo.objects.filter(status="ativo")

    for emprestimo in emprestimos:
        dic["id"] = emprestimo.id
        dic["aluno"] = emprestimo.aluno
        dic["livro"] = emprestimo.livro
        dic["prazo"] = emprestimo.data
        linhas.append(dic.copy())
        dic.clear()

    return linhas


def carrega_alunos(filtro, apenas_bloqueados):
    linhas = []
    dic = {}

    if apenas_bloqueados:
        if filtro:
            alunos = Aluno.objects.filter(nome__contains=filtro).filter(status="bloqueado")
        else:
            alunos = Aluno.objects.filter(status="bloqueado")
    else:
        if filtro:
            alunos = Aluno.objects.filter(nome__contains=filtro)
        else:
            alunos = Aluno.objects.all()

    for aluno in alunos:
        dic["matricula"] = aluno.matricula
        dic["nome"] = aluno.nome
        dic["periodo"] = aluno.periodo
        dic["ano"] = aluno.ano
        if apenas_bloqueados:
            locale.setlocale(locale.LC_ALL, '')
            dic["valor"] = locale.currency(aluno.valor_debito)
        linhas.append(dic.copy())
        dic.clear()

    return linhas

