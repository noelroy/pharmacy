from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    details = models.TextField(max_length=500)


    class Meta:
        db_table = 'medicine'

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    @staticmethod
    def get_medicines():
        medicines = Medicine.objects.all()
        return medicines
