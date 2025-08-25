from django.shortcuts import render, redirect
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
    if request.method == "GET":
        return render(request, 'cadastro_produto.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')
        quantidade = request.POST.get('quantidade')

        produto = Produto(
            nome = nome,
            preco = preco,
            quantidade = quantidade,
        )
        produto.save()
        return redirect('url_produto')
