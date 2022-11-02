from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"HEAD"),(2,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHEAD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_images')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_images')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=False, blank=False)
    id=models.AutoField(primary_key=True)
    
    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=100.00)
    image = models.ImageField(upload_to = 'product_img',  blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    slug = models.CharField(max_length=150, null=False, blank=False)
    id=models.AutoField(primary_key=True)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name
