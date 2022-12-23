from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


SUCCESS = 1
ON_THE_WAY = 2
PENDING =3
CANCEL = 4
ORDER_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (ON_THE_WAY, 'On the way'),
        (PENDING,'Pending'),
        (CANCEL, 'Cancel order')
)


class TimeStampedModel(models.Model):
     created_on = models.DateTimeField(auto_now_add=True)
     updated_on = models.DateTimeField(auto_now=True)
     class Meta:
         abstract = True


'''class User(AbstractUser):
     is_restaurant = models.BooleanField(default=False)
     is_user = models.BooleanField(default=False)'''

  
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name


class MenuCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, related_name="categories", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name


class MenuItem(TimeStampedModel):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "images/")
    is_available = models.BooleanField(default = True)
    is_veg = models.BooleanField(default = True)

    def __str__(self):
        return '{} {} {} {}'.format(self.category,self.name, self.restaurant,self.price)


class Cart(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField(default=0)
    cart_status = models.IntegerField(default = 3,choices = ORDER_STATUS_CHOICES) 
    is_active = models.BooleanField(default = True)
    subtotal = models.IntegerField(default = 0)
    
    def __str__(self):
        return '{} '.format(self.menu_items)


class Order(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    tax =  models.FloatField(default = 0.1)
    total = models.IntegerField(default = 0)
    phone_number = models.CharField(max_length = 10)
    address = models.CharField(max_length=50)
    order_status = models.IntegerField(default = 1,choices = ORDER_STATUS_CHOICES) 
    status = models.BooleanField(default = True)


class Payment(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    transaction_id = models.TextField(max_length=200)
    paid_status =  models.IntegerField(default = 3,choices = ORDER_STATUS_CHOICES)
    amount = models.IntegerField()
    email = models.EmailField()
  


