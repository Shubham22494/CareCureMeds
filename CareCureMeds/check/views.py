from django.shortcuts import render
from django.http import HttpRequest

from check.models import Customer,Medicine
from django.http import request
from django.db import transaction

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from check.models import Customer,Cart
def homec(request,email):
    medicines = Medicine.objects.all()
    # customer=Customer.objects.get(email=email, password=password)
    # customer_image=customer.img
    customer=Customer.objects.get(email=email)
    customer_image=customer.img.url
    # customer=request.session.get('customer')
    
    return render(request,'homec.html',{'medicines':medicines,'customer_image':customer_image,'email':email})
def loginc(request):
    return render(request,"loginc.html")
def login(request):
    if request.method=='POST':
        email=request.POST['username']
        password=request.POST['password']
        request.session.setdefault('login_attempts', 0)
        
        messi = 'This email id does not exist. Sign up to register this email id or use an already registered email id!!'
        try:
            Customer.objects.get(email=email)
            request.session['customer_image']=None
            request.session['customer']=None
        except Customer.DoesNotExist:
            return render(request, 'loginc.html', {'error_message': messi})

        try:
            customer = Customer.objects.get(email=email, password=password)
            
            
            if customer:
                
                request.session['login_attempts'] = 0
                
               
                request.session['cart'] = []
                # if 'cart' not in request.session:
                #     request.session['cart'] = []
                request
                customer_image = customer.img.url if customer.img else None
                request.session['customer_image']=customer_image
                request.session['customer']=customer.email
                
                
                
                return redirect('homec',email)
        except Customer.DoesNotExist:
            
            request.session.setdefault('login_attempts', 0)
            request.session['login_attempts'] += 1
            print(request.session['login_attempts'] )
            
           
            # messages.warning(request, 'Incorrect email or password. Please try again.')
            
            
            if request.session['login_attempts'] >= 3:
                
               user_email = email
               try:
                    user = Customer.objects.get(email=user_email)
                    user.delete()
                    mess = 'Your account has been deleted due to 3 consecutive failed login attempts!!!! Register again.'
                    return render(request, 'loginc.html', {'error_message': mess})

               except Customer.DoesNotExist:
                   
                    pass
               
                # mess='3 Login attempts failed'
                # return render(request,'loginc.html',{'error_message': mess})
    
    
    return redirect('loginc')
        # if(Customer.objects.get(email=email, password=password)==True):
        #     customer = Customer.objects.get(email=email, password=password)
        # else:
        #     print("customer does not exist")
        #     return redirect('loginc')  # Redirecting back to the login page
        # if 'cart' not in request.session:
        #     request.session['cart'] = []
        # if customer is not None:
        #     return redirect('homec')
        
# def registeruser(request):
   
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         middle_name = request.POST['middle_name']
#         last_name = request.POST['last_name']
#         address = request.POST['address']
#         city = request.POST['city']
#         state = request.POST['state']
#         zip_code = request.POST['zip']
#         phone_no = request.POST['phone_no']
#         email = request.POST['email']
#         date_of_birth = request.POST['date_of_birth']
#         is_premium = request.POST.get('isPremium',False) == 'on' 
#         password = request.POST['password']
#         img = request.FILES.get('img')

#         if Customer.objects.filter(email=email).exists():
#             # messages.error(request, 'Email is already in use. Please choose another email.')
#             mess='Email is already in use. Please choose another email.'
#             return render(request, 'registeruser.html',{'error_message':mess})
#         new_customer = Customer(
#             first_name=first_name,
#             middle_name=middle_name,
#             last_name=last_name,
#             address=address,
#             city=city,
#             state=state,
#             zip=zip_code,
#             phone_no=phone_no,
#             email=email,
#             date_of_birth=date_of_birth,
#             isPremium=is_premium,
#             password=password,
#             img=img
#         )

       
#         new_customer.save()

       
#         return redirect('/')
#     else:
        
        
#         return render(request,'registeruser.html')

@transaction.atomic
def registeruser(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                first_name = request.POST['first_name']
                middle_name = request.POST['middle_name']
                last_name = request.POST['last_name']
                address = request.POST['address']
                city = request.POST['city']
                state = request.POST['state']
                zip_code = request.POST['zip']
                phone_no = request.POST['phone_no']
                email = request.POST['email']
                date_of_birth = request.POST['date_of_birth']
                is_premium = request.POST.get('isPremium', False) == 'on'
                password = request.POST['password']
                img = request.FILES.get('img')

                if Customer.objects.filter(email=email).exists():
                    mess = 'Email is already in use. Please choose another email.'
                    return render(request, 'registeruser.html', {'error_message': mess})

                new_customer = Customer(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    address=address,
                    city=city,
                    state=state,
                    zip=zip_code,
                    phone_no=phone_no,
                    email=email,
                    date_of_birth=date_of_birth,
                    isPremium=is_premium,
                    password=password,
                    img=img
                )

                new_customer.save()

                return redirect('/')
        except Exception as e:
            # Handle exceptions here, such as database errors
            # You can log the error or display a custom error message
            print(e)
            error_message = 'An error occurred while processing your request. Please try again later.'
            return render(request, 'registeruser.html', {'error_message': error_message})
    else:
        return render(request, 'registeruser.html')
def add_tocart(request,email):
    if request.method == 'POST':
        
        medicine_id = request.POST.get('medicine_id')
        
        
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        
        if 'cart' not in request.session:
            request.session['cart'] = []
        cart1,created=Cart.objects.get_or_create(customer_email=email)
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        cart1.medicine_ids.add(medicine)
        print(cart1.medicine_ids)
        cart = request.session.get('cart', [])
        for item in cart:
            if item['id'] == medicine.medicine_id:
                
                item['quantity'] += 1
                break
        else:
            
            cart.append({
                'id': medicine.medicine_id,
                'name': medicine.name,
                'price': str(medicine.price),
                'image_url': medicine.image_url,
                'quantity': 1,
            })
        
       
        request.session['cart'] = cart
        # print(cart)
        
        return redirect('homec',email)
    else:
        
        return redirect('homec',email) 
def showCart(request,email):
    if request.method=="POST":
        cart=request.session.get('cart')
        cart1=Cart.objects.get(customer_email=email)
        
        total = 0
        if not cart:  
            
            return render(request, 'cart.html', {'empty_cart': True,'email':email})
        
        for item in cart:
            medicine = Medicine.objects.get(pk=item['id'])
            if medicine.amount <item['quantity']:
                messages.error(request, f"Not enough stock available for {medicine.name}.\n Remove the item to continue payment")
            total += float(item['price']) * item['quantity']
        return render(request,'cart.html',{'cart':cart,'total':total,'email':email})
# def proceed_to_payment(request):
#     if request.method == 'POST':
#         cart = request.session.get('cart', [])
        
        
#         for item in cart:
#             try:
#                 medicine = Medicine.objects.get(pk=item['id'])
#                 if medicine.amount >= item['quantity']:
#                     medicine.amount = (medicine.amount)-item['quantity']
#                     medicine.save()
#                     del request.session['cart']
#                     return render(request, 'payment.html')
                    
                    
#                 else:
                   
#                     messages.error(request, f"Not enough stock available for {medicine.name}.\n Remove the item to continue payment")
#                     return render(request,'cart.html')  
#             except Medicine.DoesNotExist:
               
#                 messages.error(request, f"Medicine with ID {item['id']} does not exist")
#                 return redirect('cart') 
#         del request.session['cart']
#         return render(request, 'payment.html')
    
   
#     return redirect('homec') 



@transaction.atomic
def proceed_to_payment(request,email):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        
        try:
            with transaction.atomic():
                for item in cart:
                    try:
                        medicine = Medicine.objects.select_for_update().get(pk=item['id'])
                        if medicine.amount >= item['quantity']:
                            medicine.amount -= item['quantity']
                            medicine.save()
                        else:
                            messages.error(request, f"Not enough stock available for {medicine.name}.\n Remove the item to continue payment")
                            return render(request, 'cart.html')
                    except Medicine.DoesNotExist:
                        messages.error(request, f"Medicine with ID {item['id']} does not exist")
                        return redirect('cart')

                del request.session['cart']
                return render(request, 'payment.html',{'email':email})
        except:
            transaction.set_rollback(True)
            
            return redirect('homec')
    
    return redirect('homec')

def remove_from_cart(request, medicine_id,email):
    if request.method == "POST":
        cart = request.session.get('cart')
        if not cart:
            return render(request, 'cart.html', {'empty_cart': True,'email':email})
        if cart:
            
            for item in cart:
                if item['id'] == medicine_id:
                    cart.remove(item)
                    break
            request.session['cart'] = cart
            if not cart:
                return render(request, 'cart.html', {'empty_cart': True,'email':email})
            
        
            
            
    total=0
    for item in cart:
            total += float(item['price']) * item['quantity']
            return render(request,'cart.html',{'cart':cart,'total':total})
   
    # return render(request,'cart.html')

from django.db import connection

def cart_trigger():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TRIGGER reduce_medicine_quantity AFTER INSERT ON medicine
            FOR EACH ROW
            BEGIN
                UPDATE Medicine
                SET amount = amount - NEW.quantity
                WHERE id = NEW.medicine_id;
            END;
        """)


def create_failed_login_trigger():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TRIGGER failed_login_trigger 
            AFTER INSERT ON customer
            FOR EACH ROW
            BEGIN
                DECLARE attempts INT;
                SET attempts = (SELECT COUNT(*) FROM customer WHERE user_id = NEW.user_id AND success = 0);
                IF attempts >= 3 THEN
                    DELETE FROM your_user_table WHERE id = NEW.user_id;
                END IF;
            END;
        """)

def customerprofile(request, email):
   
    customer = Customer.objects.get(email=email)
    
    
    return render(request, 'customerprofile.html', {'customer': customer})