from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AdminHEAD)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Order)
