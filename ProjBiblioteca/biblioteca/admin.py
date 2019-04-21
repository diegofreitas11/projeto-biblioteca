from django.contrib import admin
from .models import Aluno, Livro, Emprestimo, Usuario

admin.site.register(Aluno)
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Usuario)

# Register your models here.
