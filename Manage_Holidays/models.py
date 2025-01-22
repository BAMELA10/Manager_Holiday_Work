from django.db import models
from Account.models import User , UserManager
from Manage_Hours import models as mds
import datetime as dt
# Create your models here.



# Models for the holidays
class Holiday(models.Model):
    code = models.CharField(max_length=30,  unique=True,default='',verbose_name="Code")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.CharField(max_length=30, default="waiting", verbose_name="Status")
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Beneficiary")
    
    
    class Meta:
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'
    
    def save(self, *args, **kwargs):
        if not self.code:  # Générer un code seulement si le champ est vide
            self.code = mds.generate_code("Ho")
        super(Holiday, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.start_date.strftime("%d/%m/%Y") + ' - ' + self.end_date.strftime("%d/%m/%Y")
    
    def reported_holiday(self):
        if self.status == "waiting" and self.start_date < dt.date.today():
            self.status == "reported"
        
    @property
    def duration(self):
        return self.end_date - self.start_date

# Models of Departure_resquest
class Departure_resquest(models.Model):
    code = models.CharField(max_length=30,  unique=True,default='',verbose_name="Code")
    departure_date = models.DateField(verbose_name="Departure Date")
    return_date = models.DateField(verbose_name="Return Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    status = models.CharField(max_length=30,default="waiting",verbose_name="Status")
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Beneficiary")
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE, verbose_name="Holiday")
    
    
    class Meta:
        verbose_name = 'Departure Resquest'
        verbose_name_plural = 'Departure Resquests'
    
    def save(self, *args, **kwargs):
        if not self.code:  # Générer un code seulement si le champ est vide
            self.code = mds.generate_code("Dp")
        super(Departure_resquest, self).save(*args, **kwargs)
    
    @property
    def duration(self):
        return self.return_date - self.departure_date
        
# Models of Permission
class Permission(models.Model):
    code = models.CharField(max_length=30,  unique=True,default='',verbose_name="Code",)
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    status = models.CharField(max_length=30,  unique=True, verbose_name="Status")
    reason = models.CharField(max_length=30,  unique=True, verbose_name="Reason")
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Beneficiary")
    

    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        
    def save(self, *args, **kwargs):
        if not self.code:  # Générer un code seulement si le champ est vide
            self.code = mds.generate_code("P")
        super(Permission, self).save(*args, **kwargs)
    
    @property
    def duration(self):
        return self.end_date - self.start_date
