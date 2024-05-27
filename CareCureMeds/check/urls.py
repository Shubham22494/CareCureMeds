from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.loginc,name='loginc'),
    path('registeruser',views.registeruser,name='registeruser'),
    path('loginc',views.loginc,name='loginc'),
    path('homec/<str:email>/',views.homec,name='homec'),
    path('login',views.login,name='login'),
    path('add_tocart/<str:email>/',views.add_tocart,name='add_tocart'),
    path('showCart/<str:email>/',views.showCart,name='showCart'),
    path('proceed_to_payment/<str:email>/',views.proceed_to_payment,name='proceed_to_payment'),
    path('remove_from_cart/<int:medicine_id>/<str:email>/',views.remove_from_cart,name='remove_from_cart'),
    path('customerprofile/<str:email>/',views.customerprofile,name='customerprofile'),
    
    # path('login')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
