from django.db import models
from phone_field import PhoneField

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200,null = True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8)
    quantidade = models.PositiveIntegerField("Quantidade", default=0, null=True)
    def __st__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=200, null = True)
    email = models.CharField("Email", max_length=200, unique=True)
    def __str__(self):
        return str(self.nome)
 #   1:1 com modeloPerfilCliente
class Perfil(models.Model):
    rua = models.CharField("Rua", max_length=200, null=True)
    numero = models.PositiveIntegerField("Numero", max_length=10)
    cep = models.CharField("CEP", max_length=10)
    bairro = models.CharField("Bairro", max_length=50)
    cidade = models.CharField("Cidade", max_length=50)
    complemento = models.CharField("Complemento", max_length=50)
    telefone = PhoneField("Telefone", max_length=11, null=True)
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name="PerfilCliente"
    )
    def __str__(self):
        return str(self.cliente)
#   1:1 Cliente
class Venda(models.Model):
    data = models.DateTimeField("Data", null=True)
    venda = models.ManyToManyField( itemVenda, through='itemVenda')
    cliente = models.ForeignKey("Venda", on_delete=models.CASCADE, related_name="vendaCliente")
    def __str__(self):
        return str(self.cliente)
    #chave estrangeira de Cliente
class itemVenda(models.Model):
    #Chave estrangeira de Venda e Produto
    quantidade = models.IntegerFiel("Quantidade", null=True)
    itemVenda = models.ForeignKey("Venda", on_delete=models.CASCADE, related_name="itemVenda")
    itemProduto = models.ForeignKey("Produto", on_delete=models.CASCADE, related_name="itemVendaProduto")
    def __str__(self):
        return str(self.itemVenda)