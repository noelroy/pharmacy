from django.db import models
from useradmin.models import Medicine

# Create your models here.
class CompanyStock(models.Model):
    batch_no = models.CharField(max_length=30)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    mfd_date = models.DateField(auto_now_add=True)
    exp_date = models.DateField()
    price = models.FloatField()
    quantity = models.IntegerField()
    sold = models.IntegerField(default=0)


class Meta:
    db_table = 'company_stock'

def __str__(self):
    return self.batchno + '-' + self.medicine