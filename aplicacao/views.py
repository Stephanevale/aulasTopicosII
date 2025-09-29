from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Cliente, Perfil, Produto, Venda, ItemVenda, Avaliacao
import pandas as pd
import io, urllib, base64, matplotlib, numpy

def index(request):
    context = {
        'texto': "olá mundo",
    }
    return render(request, 'index.html', context)
@login_required(login_url="url_entrar")
def produto(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render(request, 'produto.html', context)

def cadastro_produto(request):
    if request.user.is_authenticated:    
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
            return redirect(('url_produto'))
    else: 
        return redirect('url_entrar')

def atualizar_produtos(request, id):
    #prod = Produto.objects.get(id = id)
    prod = get_object_or_404(Produto, id=id)
    if request.method == "GET":
        context = {
            'prod': prod,
        }
        return render(request, 'atualizar_produtos.html', context)
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')     
        quantidade = request.POST.get('quantidade')   

        prod.nome = nome
        prod.preco = preco
        prod.quantidade = quantidade
        prod.save()
    return redirect('url_produto')

def apagar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    prod.delete()
    return redirect('url_produto')

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return  redirect('url_produto')
        else:
            return HttpResponse("Falha no login")

def cadastro_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email= request.POST.get('email')

        user = User.objects.filter(username=nome).first()
        if user:
            return HttpResponse("Usuário existe")
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, "Usuário cadastrado") 
        return render(request, "entrar.html")
    else:
        return render(request, 'cadastro_user.html')

def cadastro_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        complemento = request.POST.get('complemento')
        telefone = request.POST.get('telefone')

        if Cliente.objects.filter(email=email).exists():
            messages.error(request, "Esse e-mail já está cadastrado!")
            return redirect("url_produto")
        
        cliente = Cliente.objects.create(nome=nome, email=email)

        Perfil.objects.create(
            cliente = cliente,
            cep=cep,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            complemento=complemento,
            telefone=telefone
            )
        
        messages.success(request, "Cliente cadastrado com sucesso.")
        return redirect('url_produto')
    return render(request, 'cadastro_cliente.html')

def vendas(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    if request.method == "POST":
        cliente_id = request.POST.get('cliente')
        cliente = Cliente.objects.get(id=cliente_id)
        venda = Venda.objects.create(cliente=cliente)

        produtos_selecionados = request.POST.getlist('produto')

        for produto in produtos:
            if str(produto.id) in produtos_selecionados:
                quantidade_str = request.POST.get(f'quantidade_{produto.id}')
                try:
                    quantidade = int(quantidade_str)
                except (ValueError, TypeError):
                    quantidade = 0

                if quantidade > 0:
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade
                    )
                    produto.quantidade -= quantidade
                    produto.save()
        messages.success(request, "Sua venda foi registrada")
    return render(request, 'vendas.html', {'clientes': clientes, 'produtos': produtos})

def sair(request):
    logout(request)
    return redirect('url_entrar')


def get_dataframe():
    avaliacoes = Avaliacao.objects.all().values()
    df = pd.DataFrame(list(avaliacoes))
    return df
    
def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

def usuarios_mais_ativos(request):
    df = get_dataframe()
    return render(request, 'usuarios_mais_ativos.html')
    nomes = df['profile_name']
    print(nomes)
def evolucao_ao_longo_do_tempo():
    pass
def preco_vs_nota():
    pass
def analise_sentimento_simples():
    pass