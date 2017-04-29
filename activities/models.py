from django.db import models
from useradmin.models import Medicine
from authentication.models import Profile


# Create your models here.
class Order(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_user')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    approval = models.NullBooleanField(null=True)

    def __str__(self):
        return self.from_user.name + '-' + self.to_user.name + '-' + self.medicine.name

    def is_approval_none(self):
        if self.approval==None:
            return True
        else:
            return False