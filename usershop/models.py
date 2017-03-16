from django.db import models
from useradmin.models import Medicine
from authentication.models import Profile

# Create your models here.


class ShopStock(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    sup_date = models.DateField(auto_now_add=True)
    exp_date = models.DateField()
    price = models.FloatField()
    quantity = models.IntegerField()
    sold = models.IntegerField(default=0)


    class Meta:
        db_table = 'shop_stock'

    def __str__(self):
        return str(self.pk) + '-' + self.medicine.name

    def get_available(self):
        return self.quantity-self.sold