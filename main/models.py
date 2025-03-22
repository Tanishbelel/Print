from django.db import models
from django.contrib.auth.models import User
import uuid
from decimal import Decimal

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'Student'
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Vendor'
    
    def __str__(self):
        return self.shop_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)  # Add this line
    payment_method = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    def get_total(self):
        return self.price * self.quantity

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.product_name} - {self.user.username}'s cart"
    
class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled')
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    total_tickets = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class PrintJob(models.Model):
    PRINT_TYPE_CHOICES = [
        ('bw', 'Black & White'),
        ('color', 'Color')
    ]
    PRINT_SIDE_CHOICES = [
        ('single', 'Single Sided'),
        ('double', 'Double Sided')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='print_documents/')
    print_type = models.CharField(max_length=10, choices=PRINT_TYPE_CHOICES)
    print_side = models.CharField(max_length=10, choices=PRINT_SIDE_CHOICES)
    copies = models.PositiveIntegerField(default=1)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document_title} - {self.user.username}"
        
    def calculate_price(self):
        # Base pricing logic
        base_price = Decimal('0.10')  # Base price per page
        
        # Adjust for color
        if self.print_type == 'color':
            base_price = Decimal('0.50')  # Higher price for color prints
            
        # Adjust for double-sided (slight discount)
        if self.print_side == 'double':
            base_price = base_price * Decimal('0.9')  # 10% discount for double-sided
            
        # Multiply by copies
        total_price = base_price * Decimal(self.copies)
        
        return total_price
        

