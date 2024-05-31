from django.db import models
from django.contrib.auth.models import User

class Orcamento(models.Model):
  cliente = models.CharField(max_length=200)
  responsavel = models.CharField(max_length=200)
  descricao = models.TextField()
  data_orcamento = models.DateField()
  
  

  def __str__(self):
    return self.cliente
  
  def calcular_total(self):
     total = sum(item.calcular_total_item() for item in self.orcamentoitem_set.all())
     return total
class OrcamentoItem(models.Model):
  orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
  servico = models.CharField(max_length=255)
  quantidade = models.IntegerField()
  valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return self.item

  def calcular_total_item(self):
      return self.quantidade * self.valor_unitario

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username