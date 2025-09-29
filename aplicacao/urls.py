from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='url_index'),
    path('produto', views.produto, name='url_produto'),
    path('cadastro_produto', views.cadastro_produto, name="url_cadastro_produto"),
    path('atualizar_produtos/<int:id>', views.atualizar_produtos, name="url_atualizar_produtos"),
    path('apagar_produto/<int:id>', views.apagar_produto, name="url_apagar_produto"),
    path('entrar', views.entrar, name="url_entrar"),
    path('cadastro_user', views.cadastro_user, name="url_cadastro_user"),
    path('sair', views.sair, name="url_sair"),
    path('cadastro_cliente', views.cadastro_cliente, name="url_cadastro_cliente"),
    path('vendas', views.vendas, name="url_vendas"),
    path('usuarios_mais_ativos', views.usuarios_mais_ativos, name="url_usuarios_mais_ativos")
]