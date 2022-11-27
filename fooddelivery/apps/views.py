from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from apps.models import(
    Restaurant,
    MenuCategory,
    MenuItem,
    Cart,
    Order,
)
from apps.serializers import(
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    RestaurantSerializer,
    MenuCategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from rest_framework import views,viewsets
from django.contrib.auth import login
from django.contrib.auth import authenticate
from apps.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import Q,F
from django_filters.rest_framework import DjangoFilterBackend



class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (AllowAny,)


class MenuCategoryView(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        hotel = self.request.data['restaurant']
        hotel = Restaurant.objects.get(id=hotel)
        serializer.save(restaurant= hotel)


class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id','name']


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user= self.request.user, price= serializer.validated_data['menu_items'].price) 


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        #cart_obj = self.request.data['cart']
        cart_obj =Cart.objects.filter(Q(user = self.request.user) & Q(is_active = True))
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',cart_obj)
        total = cart_obj.aggregate(total = Sum(F('price') * F('quantity')))['total']
        print('tttttttttttttttttttttttttttt',total)
        cart_obj.update(is_active = False)
        serializer.save(user= self.request.user,total=total)

   





