from django.urls import path,include
from apps.views import(
    LoginView,
    RegisterUserAPIView,
)
from apps import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'hotel',views.RestaurantView)
router.register(r'category',views.MenuCategoryView)
router.register(r'item',views.MenuItemView)
router.register(r'cart',views.CartView)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('register/',RegisterUserAPIView.as_view()),
]