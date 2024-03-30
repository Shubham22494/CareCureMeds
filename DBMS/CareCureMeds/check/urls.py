from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginc,name='loginc'),
    path('registeruser',views.registeruser,name='registeruser'),
    path('loginc',views.loginc,name='loginc'),
    path('homec',views.homec,name='homec'),
    path('login',views.login,name='login'),
    path('add_tocart',views.add_tocart,name='add_tocart'),
    path('showCart',views.showCart,name='showCart'),
    path('proceed_to_payment',views.proceed_to_payment,name='proceed_to_payment'),
    path('remove_from_cart/<int:medicine_id>/',views.remove_from_cart,name='remove_from_cart'),
    # path('login')
    
]
