from django.db import models
from Account import models as user_models
import string
import random
from django.utils import timezone
import datetime as dt
# Create your models here.

def generate_code(letter):
    letter = letter
    size = 6
    caractere = string.ascii_letters.upper() +  string.digits
    code = ''.join(random.choice(caractere) for _ in range(size))
    finalCode = letter + '-' + code
    return finalCode

class plan_hours(models.Model):
    code = models.CharField(verbose_name="Code", unique=True, default='',blank=False, max_length=10)
    date_day = models.DateField(verbose_name="Day", null=False,blank=False)
    start_hours = models.TimeField(verbose_name="Start", null=False,blank=False)
    end_hours = models.TimeField(verbose_name="End", null=False,blank=False)
    employee = models.ForeignKey(user_models.User, verbose_name="Employe", null=False, blank=False, on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = "Hours of Work"
        verbose_name_plural = "Hours of Work"
    
    def __str__(self):
        return self.code
    
    def is_valid_time_range(self):
        return self.start_hours < self.end_hours
    
    def is_upcoming_day(self):
        return self.date_day > dt.date.today()
    
    def save(self, *args, **kwargs):
        if not self.code:  # Générer un code seulement si le champ est vide
            self.code = generate_code("H")
        super(plan_hours, self).save(*args, **kwargs)
    
    @property
    def duration(self):
        return self.end_hours - self.start_hours
    
# Models of Disponibility
class Disponibility(models.Model):
    code = models.CharField(verbose_name="Code", unique=True, default='',blank=False, max_length=10)
    date_day = models.DateField(verbose_name="Day", null=False,blank=False)
    Date_creation = models.DateField(verbose_name="Day of Creation", null=False,blank=False, default=dt.datetime.now())
    start_hours = models.TimeField(verbose_name="Start", null=False,blank=False)
    end_hours = models.TimeField(verbose_name="End", null=False,blank=False)
    employee = models.ForeignKey(user_models.User, verbose_name="Employe", null=False, blank=False, on_delete=models.CASCADE)
    
    Status = models.CharField(verbose_name="Status", default="waiting",blank=False, max_length=10)
    
    class Meta:
        verbose_name = 'Disponibility of Employee'
        verbose_name_plural = 'Disponibilities of Employees'
    
    def __str__(self):
        return self.code + self.date_day
    
    def is_valid_time_range(self):
        return self.start_hours < self.end_hours
    
    def is_upcoming_day(self):
        return self.date_day > dt.date.today()
    
    def save(self, *args, **kwargs):
        if not self.code:  # Générer un code seulement si le champ est vide
            self.code = generate_code("D")
        super(Disponibility, self).save(*args, **kwargs)
        
    @property
    def duration(self):
        return self.end_hours - self.start_hours
