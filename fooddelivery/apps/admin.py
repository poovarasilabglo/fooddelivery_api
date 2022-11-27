from django.contrib import admin
from apps.models import(
     Restaurant,
     MenuCategory,
     MenuItem,
     Cart,
     Order,
)


class Restaurantadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
admin.site.register(Restaurant,Restaurantadmin) 


class MenuCategoryadmin(admin.ModelAdmin):
    list_display = ('id', 'name','created_on',)
admin.site.register(MenuCategory,MenuCategoryadmin) 


class MenuItemadmin(admin.ModelAdmin):
    list_display = ('id','category','restaurant','name','price','image','restaurant','is_available','is_veg','created_on')
admin.site.register(MenuItem,MenuItemadmin) 


class Cartadmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'menu_items', 'quantity','price','is_active','cart_status','created_on','updated_on')
admin.site.register(Cart,Cartadmin) 


class Orderadmin(admin.ModelAdmin):
    list_display = ('id','user','total','status', 'created_on','updated_on')
admin.site.register(Order,Orderadmin) 










