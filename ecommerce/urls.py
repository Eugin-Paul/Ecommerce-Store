from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('register', views.register, name = 'register'),
    path('login', views.loginpage, name = 'loginpage'),
    path('logout', views.logoutpage, name = 'logoutpage'),
    path('updateitem', views.updateitem, name = 'updateitem'),
    path('processorder', views.processorder, name = 'processorder'),
]
