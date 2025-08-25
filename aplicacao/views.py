from django.shortcuts import render
from .models import Produto
from django.http.response import HttpResponse
# Create your views here.

def index(request):
    context = {
        'texto': "olá mundo",
    }
    return render(request, 'index.html', context)

def produto(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render(request, 'produto.html', context)

def cadastro_produto(request):
    return render(request, 'cadastro_produto.html')
