from django.db import models

# Create your models here.
class Aluno(models.Model):
    matricula = models.CharField(max_length=100, null=False, primary_key=True)
    nome = models.CharField(max_length=100, null=False)
    rg = models.CharField(max_length=100, null=False)
    periodo = models.CharField(max_length=100, null=False)
    ano = models.CharField(max_length=100, null=False)
    senha = models.CharField(max_length=100, null=False)
    status = models.CharField(max_length=10, null=False, default="ativo")
    valor_debito = models.FloatField(null=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, null=False)
    genero = models.CharField(max_length=50, null=False)
    autor = models.CharField(max_length=50, null=False)
    editora = models.CharField(max_length=50, null=False)
    descricao = models.CharField(max_length=150, null=True, blank=True)
    ano = models.IntegerField(null=False, default=0000)
    quantidade = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data = models.DateTimeField()
    status = models.CharField(max_length=11)

    def getNomeAluno(self):
        return self.aluno.nome

    def getNomeLivro(self):
        return self.livro.nome

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)
    login = models.CharField(max_length=10)
    senha = models.CharField(max_length=10)
    logado = models.BooleanField()

    def __str__(self):
        return self.nome