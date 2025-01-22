from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, PermissionManager, AbstractUser
from django.db import models
from django.core.mail import send_mail
from Manager_Holiday_Work import settings
from django.utils import timezone
# Create your models here.

# Models for a service of structute
class Service(models.Model):
    code = models.CharField(max_length=30,  unique=True,verbose_name="Code")
    Wording = models.CharField(max_length=30,  unique=True, verbose_name="Wording")
    Description = models.TextField(max_length=500,verbose_name="Description")
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

# Models for  User Profiles or Employers 
class UserManager(BaseUserManager):
    # Custom Manager for user of system
    
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first namee , last name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
        email=self.normalize_email(email),
        last_name = last_name,
        first_name = first_name
        )
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        
        ''' send_mail(
            "Information of account",
            "Your username is {} and your password is {}. THANKS".format(email, password),
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ) '''
        
        return user
    
    
    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first name , last name and password.
        """
        user = self.create_user(
        email = self.normalize_email(email),
        password=password,
        last_name = last_name,
        first_name = first_name
        )
        user.admin = True
        user.save(using=self._db)
        
        ''' send_mail(
            "Information of account",
            "Your username is {} and your password is {}. THANKS".format(email, password),
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ) '''
        
        return user
    


class User(AbstractUser):
    EMPLOYEE = 'Employee'
    RH = 'RH'

    ROLE_CHOICES = [
            (EMPLOYEE, 'Employee'),
            (RH, 'RH'),
        ]
    first_name = models.CharField(max_length=30,  verbose_name='First Name')
    last_name = models.CharField(max_length=30,  verbose_name='Last Name')
    email = models.EmailField(max_length=30, unique=True,verbose_name='E-mail')
    admin = models.BooleanField(default=False, verbose_name='Administrator')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    date_joined = models.DateTimeField(verbose_name="Date joined", default=timezone.now)
    username = None
    is_staff = None
    is_superuser = None
    service = models.ForeignKey(Service, on_delete=models.CASCADE,verbose_name="Service",null=True,default=None)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,verbose_name='Rôle', default=None)
    
    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["first_name","last_name","service"]
    
    objects = UserManager()
    
    
    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'
        
    def __str__(self):
        return self.first_name + ' '+ self.last_name
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin
        

     
''' class Employer(User):
    responsability = models.CharField(max_length=30, verbose_name="Responsability")
    
    
    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers' '''
# Models of Task   
class Task(models.Model):
    code = models.CharField(max_length=30,  unique=True, verbose_name="Code")
    creation_date = models.DateTimeField(verbose_name="Creation Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    start_hour = models.TimeField(verbose_name="Start Hour")
    end_hour = models.TimeField(verbose_name="End Hour")
    Comment = models.CharField(max_length=500,  unique=True)
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'