from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'texto': "olá mundo",
    }
    return render(request, 'index.html', context)

def produto(request):
    context = {
        'produto': "laranja",
    }
    return render(request, 'produto.html', context)