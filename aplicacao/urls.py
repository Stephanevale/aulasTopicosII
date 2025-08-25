from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='url_index'),
    path('produto', views.produto, name='url_produto'),
    path('cadastro_produto', views.cadastro_produto, name="url_cadastro_produto")
   #path('criar_produto', views.criar_produto, name="url_criar_produto")
]