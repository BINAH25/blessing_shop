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
                              upload_to='profile_images', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    @property
    def image_url(self):
        if self.image == "":
            self.image = ''
        return self.image
    

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_images', blank=True, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    @property
    def image_url(self):
        if self.image == "":
            self.image = ''
        return self.image
    

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
    
    @property
    def image_url(self):
        if self.image == "":
            self.image = ''
        return self.image
    
    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name

class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
    cart_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    #session_id = models.CharField(max_length=100)
    

    @property
    def num_of_items(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.quantity for qty in cartitems])
        return qtysum
    
    @property
    def cart_total(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.subTotal for qty in cartitems])
        return qtysum

    def __str__(self):
        return str(self.cart_id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    
    
    @property
    def subTotal(self):
        total = self.quantity * self.product.price
        
        return total
    
   

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    order_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)

class Review(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="test_images")
    text = models.TextField()


    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog_images")
    text =  models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
