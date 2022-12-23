from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from rest_framework import generics
from apps.models import(
    Restaurant,
    MenuCategory,
    MenuItem,
    Cart,
    Order,
    Payment,
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
    PaymentSerializer,
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
import stripe
import json
from rest_framework.views import APIView
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY


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
        serializer.save(user= self.request.user, 
                        price= serializer.validated_data['menu_items'].price) 


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart_obj =Cart.objects.filter(Q(user = self.request.user) & Q(is_active = True))
        total = cart_obj.aggregate(total = Sum(F('price') * F('quantity')))['total']
        serializer.save(user= self.request.user,total=total,cart =cart_obj)
        cart_obj.update(is_active = False)


class Checkout_Sessionview(APIView):
    def post(self, request, format=None):
        carts = Cart.objects.filter(Q(user = self.request.user) & Q(is_active = True))
        total = carts.aggregate(total = Sum(F('price') * F('quantity')))['total']
        tax = total * 0.1
        subtotal = total + tax
        created = Order.objects.create(order_status=2,user_id = self.request.user.id)
        created.cart.add(*carts)
        carts.update(is_active = False,cart_status =1)
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items =[
            {
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': int(subtotal),
                    'product_data' : {
                        'name': 'products',
                     },
                 },
                    'quantity' : 1,
                },
             ],
             metadata ={'order_id':created.id},
             mode = 'payment',
             success_url= YOUR_DOMAIN + '',
             cancel_url= YOUR_DOMAIN + '',

        ) 
        print(checkout_session)
        return redirect(checkout_session.url)


class webhook_endpoint(APIView):
    def post(self, request, format=None):
        payload = self.request.body.decode('utf-8')
        dict_obj = json.loads(payload)
        print(dict_obj['type'])
        if dict_obj['type'] == "checkout.session.completed":
            session = dict_obj['data']['object']
            sessionID = session["id"]
            customer_email = session["customer_details"]["email"]
            total = session["amount_total"] 
            order_id = session["metadata"]["order_id"]
            order_status=Order.objects.filter(id =order_id).update(order_status=1)
            payment_detail = Payment.objects.create(transaction_id = sessionID,email = customer_email, amount = total, paid_status = True, order =Order.objects.get(id =int(order_id)))
        
        elif  dict_obj['type'] == "payment_intent.payment_failed":
            session = dict_obj['data']['object']
            transaction_id = session['id']
            amount = dict_obj['data']['object']["amount"]
            #customer_email = session['billing_details']['email']
            print('Payment Failed')
        return Response(status=status.HTTP_200_OK)


class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)









