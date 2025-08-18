from django.shortcuts import render
from .models import Produto

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