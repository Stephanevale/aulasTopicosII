from django.db import models

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200,null = True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8)
    quantidade = models.PositiveIntegerField("Quantidade", default=0, null=True)
    def __st__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField("Nome", max_lenght=200, null = True)
    email = models.CharField("Email", max_length=200,null = True)
 #   1:1 com modeloPerfilCliente

 class PerfilCliente(models.Model):
    endereco = models.CharField("Endereco", max_length=200, null=True)
    telefone = models.PhoneNumberField("Telefone", max_length=11, null=True)
#   1:1 Cliente
class Venda(models.Model):
    data = models.DateTimeField("Data", null=True)
    #chave estrangeira de Cliente
    #N:N Produtos
class itemVenda(models.Model):
    #Chave estrangeira de Venda e Produto
    quantidade = models.IntegerFiel("Quantidade", null=True)
    itemVenda = models.ForeignKey(
        "Venda", on_delete=models.CASCADE, related_name="itemVenda"
        "Produto", on_delete=models.CASCADE, related_name="itemVendaProduto"
    )