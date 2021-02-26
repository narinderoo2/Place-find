from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class facility(models.Model):
    PAID = 'PD'
    UNPAID = 'UD'
    CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
    ]
    PROFESSIONAL = 'PR'
    UNPROFESSIONAL = 'UR'
    CHOICES1 = [
        (PROFESSIONAL, 'Professional'),
        (UNPROFESSIONAL, 'Unprofessional'),
    ]

    category = models.CharField(max_length=10, blank=False, )
    Name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=30, primary_key=True)
    phone = models.IntegerField()
    local = models.CharField(max_length=250)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    pincode = models.IntegerField()
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True)
    lattitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True)
    mode = models.CharField(max_length=2, choices=CHOICES, default=UNPAID, )
    field = models.CharField(max_length=2, choices=CHOICES1, default=UNPROFESSIONAL, )
    distance = models.DecimalField(max_digits=20, default="5.00", decimal_places=2)
   # image1 = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
#   image2 = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
#    image3 = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
#    image4 = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)


#Custom User As Account


class MyAccountManager(BaseUserManager):
    def create_user(self,email,fullname,password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not fullname:
            raise ValueError("Users must have an fullname")

        user=self.model(
            email=self.normalize_email(email),
            fullname=fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,fullname,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            fullname=fullname,
        )

        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

    



class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=40,unique=True)
    username=models.CharField(max_length=30,unique=True,null=True,blank=True)
    date_joined=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login",auto_now_add=True)
    is_admin=models.BooleanField(default=False)  
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    adress=models.CharField(max_length=70,blank=True,null=True)
    city=models.CharField(max_length=40,blank=True,null=True)
    state=models.CharField(max_length=40,blank=True,null=True)
    country=models.CharField(max_length=40,blank=True,null=True)
    fullname=models.CharField(max_length=40)
    

    





    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname']


    objects=MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

#Profile Model
def upload_location(instance,filename,**kwargs):
    file_path='my_app{email}/{fullname}-{filename}'.format(email=str(instance.user.email),fullname=str(instance.user.fullname),filename=filename)
    return file_path

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profileImage=models.ImageField(upload_to=upload_location,null=True,blank=True)
    updateDate=models.DateTimeField(auto_now=True,verbose_name="Profile update")
    bio=models.TextField(max_length=1000,null=True,blank=True)
    interests1=models.CharField(max_length=50,null=True,blank=True)
    interests2=models.CharField(max_length=50,null=True,blank=True)
    interests3=models.CharField(max_length=50,null=True,blank=True)
    interests4=models.CharField(max_length=50,null=True,blank=True)
    phone=models.CharField(max_length=10,null=True,blank=True,unique=True)
    slug=models.SlugField(blank=True,unique=True)
    role=(
        ('novice','NOVICE'),
        ('professional',"PROFESSIONAL"),
        ('select_role',"SELECT_ROLE")
    )
    roles=models.CharField(max_length=20,choices=role,default="select_role")
    gender=(
        ('male',"MALE"),
        ('female',"FEMALE"),
        ('others',"OTHERS"),
        ('select_gender',"SELECT_GENDER")
    )
    genders=models.CharField(max_length=20,choices=gender,default="select_gender")

    def __str__(self):
        return self.phone


@receiver(post_delete,sender=Profile)
def submission_delete(sender,instance,**kwargs):
    instance.profileImage.delete(False)

def pre_save_blog_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.user.fullname+"-"+instance.phone)    

pre_save.connect(pre_save_blog_post_receiver,sender=Profile)

