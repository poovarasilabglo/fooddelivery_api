from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from apps.models import(
    Restaurant,
    MenuCategory,
    MenuItem,
    Cart,
    Order,
    Payment,
)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = self.authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    #is_restaurant = serializers.BooleanField(default=False)
    #is_user = serializers.BooleanField(default=True)
    token = serializers.SerializerMethodField('get_user_token')

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name','token')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }
 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
 
    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_user_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address')


class MenuCategorySerializer(serializers.ModelSerializer):
    #restaurant = serializers.ReadOnlyField(source='restaurant.name')
    class Meta:
        model = MenuCategory
        fields = ['id', 'name','restaurant','created_on']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','category','restaurant','name','price','image','restaurant','is_available','is_veg','created_on']


class CartSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    subtotal = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = Cart
        fields = ['user', 'id', 'menu_items', 'quantity','price','subtotal','is_active','created_on','updated_on']

    def total(self,cartitem:Cart):
        return cartitem.quantity * cartitem.price


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','total','cart','phone_number','address','status']
        extra_kwargs = {
        'cart': {'read_only': True},
        }


class PaymentSerializer(serializers.ModelSerializer):
     user = serializers.ReadOnlyField(source='user.username')
     class Meta:
        model = Payment
        fields = ['user','order','transaction_id','paid_status','amount','email']




 
