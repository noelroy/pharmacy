from django.db import models
import os.path

from django.conf import settings
from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Max
from django.db.models import Sum
from datetime import date

# Create your models here.
@python_2_unicode_compatible
class Profile(models.Model):
    SHOP = 'S'
    COMPANY = 'C'
    INSTITUTION_TYPES = (
        (SHOP, 'Shop'),
        (COMPANY, 'Company')
    )

    user = models.OneToOneField(User)
    name = models.CharField(max_length=30, blank=True)
    license_id = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=1,choices=INSTITUTION_TYPES,blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'inst_profile'

    def __str__(self):
        return self.user.username

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def get_type(self):
        try:
            if self.user.profile.type == Profile.COMPANY:
                return 'Company'
            elif self.user.profile.type == Profile.SHOP:
                return 'Shop'
            else:
                return 'Admin'
        except:
            return ''

    def get_med_list(self,med):
        from usershop.models import ShopStock
        from usercompany.models import CompanyStock
        if(self.get_type()=='Shop'):
            stock = ShopStock.objects.filter(profile=self).filter(medicine__pk=med).filter(exp_date__gt = date.today())
            return stock
        elif(self.get_type()=='Company'):
            stock = CompanyStock.objects.filter(profile=self).filter(medicine__pk=med).filter(exp_date__gt = date.today())
            return stock
        else:
            return ''

    def get_avail_med(self):
        from usershop.models import ShopStock
        from usercompany.models import CompanyStock
        if(self.get_type()=='Shop'):
            stock = ShopStock.objects.filter(profile=self).filter(exp_date__gt = date.today()).values('medicine','medicine__name').annotate(mcount=(Sum('quantity') - Sum('sold')))
            return stock
        elif(self.get_type()=='Company'):
            stock = CompanyStock.objects.filter(profile=self).filter(exp_date__gt = date.today()).values('medicine','medicine__name').annotate(mcount=(Sum('quantity') - Sum('sold')))
            return stock
        else:
            return ''

    def get_avail_med_single(self,med):
        stock = self.get_med_list(med)
        stock = stock.values('medicine').annotate(mcount=(Sum('quantity') - Sum('sold')))
        return int(stock[0]['mcount'])

    def get_avail_med_price(self,med):
        stock = self.get_med_list(med)
        stock = stock.aggregate(price=Max('price'))
        if stock['price'] is None:
            stock['price']=0;
        return int(stock['price'])

    @staticmethod
    def get_unapproved():
        profiles = Profile.objects.filter(approved = False,user__is_staff = False).exclude(name__isnull=True).exclude(name__exact='')
        return profiles

    @staticmethod
    def get_shop():
        profiles = Profile.objects.filter(type = Profile.SHOP)
        return profiles

    @staticmethod
    def get_company():
        profiles = Profile.objects.filter(type=Profile.COMPANY)
        return profiles


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Address(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    line1 = models.CharField(max_length=50, blank=False)
    line2 = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.IntegerField()
    contactno = models.IntegerField()
    email = models.EmailField(max_length=20)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return self.line1