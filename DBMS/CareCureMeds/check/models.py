from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    phone_no = models.BigIntegerField()
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField()
    isPremium = models.BooleanField()
    password = models.CharField(max_length=255)  # Adding password field
    img = models.ImageField(upload_to='customerpics')



class Medicine(models.Model):
    MEDICINE_TYPES = [
        ('Tablet', 'Tablet'),
        ('Capsule', 'Capsule'),
        ('Liquid', 'Liquid'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
        ('Ointment', 'Ointment'),
        ('Drops', 'Drops'),
        ('Inhaler', 'Inhaler'),
        ('Powder', 'Powder'),
        ('Other', 'Other'),
    ]

    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # storage_conditions = models.CharField(max_length=255)
    expiry_date = models.DateField()
    type = models.CharField(max_length=20, choices=MEDICINE_TYPES)
    prescription_required = models.BooleanField()
    image_url = models.URLField(max_length=200)


    
