from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='url_index'),
    path('produto', views.produto, name='url_produto'),
    path('cadastro_produto', views.cadastro_produto, name="url_cadastro_produto"),
    path('atualizar_produtos/<int:id>', views.atualizar_produtos, name="url_atualizar_produtos"),
    path('apagar_produto/<int:id>', views.apagar_produto, name="url_apagar_produto"),
    path('entrar', views.entrar, name="url_entrar"),

   #path('criar_produto', views.criar_produto, name="url_criar_produto")
]