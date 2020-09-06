from django.db import models

from django.contrib.auth.models import User

class Customer(models.Model) :
    user = models.OneToOneField(User,on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length = 200, null =True)
    email = models.CharField(max_length = 200, null =True)

    def __str__(self):
        return self.name

class Product(models.Model) :
    name = models.CharField(max_length = 200, null = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)
    digital = models.BooleanField(default = False, null = True)
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try :
            url = self.image.url
        except :
            url = ''
        return url

class Order(models.Model) :
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL, null = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True)

    # def __str__(self):
    #     return self.id

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model) :
    product = models.ForeignKey(Product,on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order,on_delete = models.SET_NULL, null = True)
    date_added = models.DateTimeField(auto_now_add = True)
    quantity = models.IntegerField(default = 0, null = True)

    # def __str__(self):
    #     return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Shipping(models.Model) :
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order,on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    state = models.CharField(max_length = 200, null = True)
    zip_code = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True)


    # def __str__(self):
    #     return self.city
