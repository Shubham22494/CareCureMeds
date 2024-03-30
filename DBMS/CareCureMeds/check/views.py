from django.shortcuts import render
from django.http import HttpRequest

from check.models import Customer,Medicine
from django.http import request

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from check.models import Customer
def homec(request):
    medicines = Medicine.objects.all()
    return render(request,'homec.html',{'medicines':medicines})
def loginc(request):
    return render(request,"loginc.html")
def login(request):
    if request.method=='POST':
        email=request.POST['username']
        password=request.POST['password']
        request.session.setdefault('login_attempts', 0)
        try:
            customer = Customer.objects.get(email=email, password=password)
            
            if customer:
                
                request.session['login_attempts'] = 0
                
               
                request.session['cart'] = []
                # if 'cart' not in request.session:
                #     request.session['cart'] = []
                
                
                return redirect('homec')
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
    
    # Redirecting back to the login page
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
        
def registeruser(request):
   
    if request.method == 'POST':
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
        is_premium = request.POST.get('isPremium',False) == 'on' 
        password = request.POST['password']
        img = request.FILES.get('img')

        if Customer.objects.filter(email=email).exists():
            # messages.error(request, 'Email is already in use. Please choose another email.')
            mess='Email is already in use. Please choose another email.'
            return render(request, 'registeruser.html',{'error_message':mess})
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
    else:
        
        
        return render(request,'registeruser.html')
def add_tocart(request):
    if request.method == 'POST':
        
        medicine_id = request.POST.get('medicine_id')
        
        
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        
        if 'cart' not in request.session:
            request.session['cart'] = []
        
        
        cart = request.session.get('cart', [])
        for item in cart:
            if item['id'] == medicine.medicine_id:
                # If the medicine is already in the cart, increase its quantity
                item['quantity'] += 1
                break
        else:
            # If the medicine is not in the cart, add it
            cart.append({
                'id': medicine.medicine_id,
                'name': medicine.name,
                'price': str(medicine.price),
                'image_url': medicine.image_url,
                'quantity': 1,
            })
        
        # Update the cart in the session
        request.session['cart'] = cart
        print(cart)
        # Redirect to the home page or any other page after adding to cart
        return redirect('homec')
    else:
        # Handle invalid requests (e.g., GET requests)
        return redirect('homec')  # Redirect to the home page
def showCart(request):
    if request.method=="POST":
        cart=request.session.get('cart')
        total = 0
        if not cart:  # Check if the cart is empty
            # Render the cart template with an alert for an empty cart
            return render(request, 'cart.html', {'empty_cart': True})
        for item in cart:
            total += float(item['price']) * item['quantity']
        return render(request,'cart.html',{'cart':cart,'total':total})
def proceed_to_payment(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        
        # Update the quantity of each item in the cart in the database
        for item in cart:
            try:
                medicine = Medicine.objects.get(pk=item['id'])
                if medicine.amount >= item['quantity']:
                    medicine.amount = (medicine.amount)-item['quantity']
                    medicine.save()
                    del request.session['cart']
                    return render(request, 'payment.html')
                    
                    
                else:
                    # If the quantity in the cart is more than available, show a message
                    messages.error(request, f"Not enough stock available for {medicine.name}.\n Remove the item to continue payment")
                    return render(request,'cart.html')  # Redirect back to the cart page
            except Medicine.DoesNotExist:
                # Handle the case where the medicine is not found in the database
                messages.error(request, f"Medicine with ID {item['id']} does not exist")
                return redirect('cart')  # Redirect back to the cart page
        
        del request.session['cart']
        return render(request, 'payment.html')
    
    # Handle invalid requests (e.g., GET requests)
    return redirect('homec')  # Redirect to the home page
def remove_from_cart(request, medicine_id):
    if request.method == "POST":
        cart = request.session.get('cart')
        if cart:
            
            for item in cart:
                if item['id'] == medicine_id:
                    cart.remove(item)
                    break
            request.session['cart'] = cart
    
    return render(request,'cart.html')

