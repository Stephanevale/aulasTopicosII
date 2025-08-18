from django.contrib import admin
from .models import Produto

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade')

admin.site.register(Produto, ProdutoAdm)
