from django.db import models
from django.contrib.auth.models import User


SUCCESS = 1
PENDING = 2
CANCEL = 3
ORDER_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (PENDING, 'Pending order'),
        (CANCEL, 'cancel order')
)


class TimeStampedModel(models.Model):
     created_on = models.DateTimeField(auto_now_add=True)
     updated_on = models.DateTimeField(auto_now=True)
     class Meta:
         abstract = True


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
    category = models.ForeignKey(MenuCategory, related_name="foods", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="food", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "images/")
    is_available = models.BooleanField(default = True)
    is_veg = models.BooleanField(default = True)

    def __str__(self):
        return '{} {}'.format(self.category, self.restaurant)


class Cart(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField(default=0)
    cart_status = models.IntegerField(default = 2,choices = ORDER_STATUS_CHOICES) 
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return '{} {}'.format(self.menu_items,self.user)


class Order(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    order_status = models.IntegerField(default = 1,choices = ORDER_STATUS_CHOICES) 
    tax =  models.FloatField(default = 0.1)
    status = models.BooleanField(default = False)

        



