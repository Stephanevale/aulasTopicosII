from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Cliente, Perfil, Produto, Venda, ItemVenda, Avaliacao
import pandas as pd
import io, urllib, base64, os
import numpy as np 
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

def index(request):
    return render(request, 'index.html')
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
    current_dir = os.path.dirname(os.path.abspath(__file__))

    base_dir = os.path.dirname(current_dir)

    file_path = os.path.join(base_dir, 'books-15k.csv')

    
    df = pd.read_csv(file_path)

    return df
    
def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    return string

def usuarios_mais_ativos(request):
    df = get_dataframe()
    nomes = df['profile_name']
    nomes = nomes.replace(['Unknown'], np.nan)
    nomes_filtrados = nomes.dropna()
    contagem_valores = (nomes_filtrados.value_counts().nlargest(15).sort_values(ascending=True))
    
    grafico = plt.figure(figsize=(10, 6))
    plt.barh(contagem_valores.index.astype(str), contagem_valores.values, color='#1f77b4')
    plt.title('Top 15 usuários mais ativos')
    plt.ylabel('Usuários')
    plt.xlabel('Número de Avaliações"')
    plt.grid(True, alpha = 0.2)
    plt.tight_layout()

    imagem_base64 = plot_to_base64(grafico)
    plt.close(grafico)

    context = {'grafico': imagem_base64}

    return render(request, 'usuarios_mais_ativos.html', context)

def evolucao_ao_longo_do_tempo(request):
    df = get_dataframe()
    df['data_review'] = pd.to_datetime(df['review_time'], unit='s')
    df['ano'] = df['data_review'].dt.year
    df['ano'].value_counts().sort_index()
    avaliacao_cada_ano = df['ano'].value_counts().sort_index()

    evolucao = plt.figure(figsize=(8, 4))
    plt.plot(avaliacao_cada_ano.index, avaliacao_cada_ano.values, marker='o', linestyle='--', color='b')
    plt.title('Evolução do Número de Avaliações por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(True, alpha =0.2)
    plt.tight_layout()

    imagem_base64 = plot_to_base64(evolucao)
    plt.close(evolucao)

    context = {'evolucao': imagem_base64}
    return render(request, 'grafico_evolucao_reviews.html', context)

def preco_vs_score(request):
    df = get_dataframe()
    df = df[df['price'] > 0].sample(n=1000)
    preco_score = plt.figure(figsize=(10, 5))
    plt.scatter(df['price'], df['review_score'], alpha=0.3)
    plt.title('Correlação entre Preço e Nota da Avaliação')
    plt.xlabel('Preço')
    plt.ylabel('Nota da Avaliação')
    plt.grid(True)

    imagem_base64 = plot_to_base64(preco_score)
    plt.close(preco_score)

    context = {'preco_score': imagem_base64}
    return render(request, 'grafico_preco_score.html', context)

def sentimento_reviews(request):
    df = get_dataframe()
    df['review_summary'] = df['review_summary'].fillna('').str.lower()

    lista_positivas = ['good', 'great', 'excellent', 'i loved', 'i recommend', 'perfect', 'wonderful', 'sucess', 'pleasant','fine', 'dope', 'fantastic','amazing']
    lista_negativas = ['bad', 'terrible', 'disappointing', "i didn't like it", 'horrible', 'hated', 'horrible','awful', 'poor', 'dreadful', 'appalling']

    
    def recebe_texto(texto):
        for palavra in lista_positivas:
            if palavra in texto:
                return 'Positivo'
        for palavra in lista_negativas:
            if palavra in texto:
                return 'Negativo'
        return 'Neutro'
    df['sentimento'] = df['review_summary'].apply(recebe_texto)
    contagem_sentimentos = df['sentimento'].value_counts()

    labels = contagem_sentimentos.index
    valores = contagem_sentimentos.values
    sentimento = plt.figure(figsize=(7, 7))
    explode = (0.1, 0, 0, 0)
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=45, colors=['blue', 'green', 'red'])
    plt.title('Distribuição de Sentimentos nos Sumários das Avaliações')
    plt.axis('equal')

    imagem_base64 = plot_to_base64(sentimento)
    plt.close(sentimento)

    context = {'sentimento': imagem_base64}
    return render(request, 'grafico_sentimento.html', context)
