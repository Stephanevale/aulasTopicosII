from django.db import models
from phone_field import PhoneField

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200,null = True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8)
    quantidade = models.PositiveIntegerField("Quantidade", default=0, null=True)
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=200, null = True)
    email = models.CharField("Email", max_length=200, unique=True)
    def __str__(self):
        return str(self.nome)


class Perfil(models.Model):
    rua = models.CharField("Rua", max_length=200, null=True)
    numero = models.PositiveIntegerField("Numero")
    cep = models.CharField("CEP", max_length=10)
    bairro = models.CharField("Bairro", max_length=50)
    cidade = models.CharField("Cidade", max_length=50)
    complemento = models.CharField("Complemento", max_length=50, null=True, blank=True)
    telefone = PhoneField("Telefone", null=True)
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name="PerfilCliente"
    )
    def __str__(self):
        return f'{self.rua}, {self.numero}'


class Venda(models.Model):
    data = models.DateTimeField("Data", null=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="vendas"
    )

    def __str__(self):
        return f"Venda {self.id} para {self.cliente}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE, related_name="itens"
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="itens_venda"
    )
    quantidade = models.IntegerField("Quantidade", null=True)

    def __str__(self):
        return f"{self.quantidade}x {self.produto} (Venda {self.venda.id})"