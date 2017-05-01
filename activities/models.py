from django.db import models
from useradmin.models import Medicine
from authentication.models import Profile
from django.utils.html import escape


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


class Transaction(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_user_trans')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_user_trans')
    quantity = models.PositiveIntegerField()
    trans_date = models.DateField(auto_now_add=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.from_user.name + '-' + self.to_user.name + '-' + self.medicine.name

class Notification(models.Model):
    ORDER_DECLINED = 'D'
    ORDER_ACCEPTED = 'A'
    STOCK_LOW = 'L'
    STOCK_EXPIRED = 'E'
    NOTIFICATION_TYPES = (
        (ORDER_DECLINED, 'Declined'),
        (ORDER_ACCEPTED, 'Accepted'),
        (STOCK_LOW, 'Low'),
        (STOCK_EXPIRED, 'Expired'),
        )

    _ORDER_DECLINED_TEMPLATE = '<a href="/user/{0}">{1}</a> declined your order for: {2}'
    _ORDER_ACCEPTED_TEMPLATE = '<a href="/user/{0}">{1}</a> accepted your order for: {2}'
    _STOCK_LOW_TEMPLATE = 'Stock low for: {0} <a href="/activities/orders/create">Place Order Here</a>. '
    _STOCK_EXPIRED_TEMPLATE = 'Stock expired for : {0} <a href="/{1}/">Delete Stock Now</a>. '

    from_user = models.ForeignKey('authentication.Profile', related_name='n_from')
    to_user = models.ForeignKey('authentication.Profile', related_name='n_to')
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True)
    medicine = models.ForeignKey('useradmin.Medicine', null=True, blank=True)
    stock = models.ForeignKey('usershop.ShopStock', null=True, blank=True)
    notification_type = models.CharField(max_length=1,
                                         choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.ORDER_DECLINED:
            return self._ORDER_DECLINED_TEMPLATE.format(
                escape(self.from_user.user.username),
                escape(self.from_user.name),
                self.order.medicine.name,
                )
        elif self.notification_type == self.ORDER_ACCEPTED:
            return self._ORDER_ACCEPTED_TEMPLATE.format(
                escape(self.from_user.user.username),
                escape(self.from_user.name),
                self.order.medicine.name,
                )
        elif self.notification_type == self.STOCK_LOW:
            return self._STOCK_LOW_TEMPLATE.format(
                escape(self.medicine.name),
                )
        elif self.notification_type == self.STOCK_EXPIRED:
            return self._STOCK_EXPIRED_TEMPLATE.format(
                escape(self.stock.medicine.name),
                escape(self.stock.pk),
                )
        else:
            return 'Ooops! Something went wrong.'
