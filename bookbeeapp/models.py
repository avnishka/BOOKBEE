from django.db import models
from django.contrib.auth.models import User
import re  # <--- Needed for Pincode logic

# --- 1. BOOK MODEL (Merged Logic) ---
class Book(models.Model):
    STATUS_CHOICES = [('AVAILABLE', 'Available'), ('LENDED', 'Lended'), ('SOLD', 'Sold')]
    TRANSACTION_CHOICES = [('rent', 'For Rent'), ('buy', 'For Sale')]
    
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Academic', 'Academic'),
        ('Fantasy', 'Fantasy'),
        ('Biography', 'Biography'),
        ('Self-Help', 'Self-Help'),
        ('Thriller', 'Thriller'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Rent per day or Sale price")
    security_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, blank=True, null=True)
    
    # Location & Pincode
    location = models.CharField(max_length=150)
    pincode = models.CharField(max_length=6, blank=True)
    
    description = models.TextField(blank=True, null=True)
    
    # Genre
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Fiction') 

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, default='rent')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    
    # Availability Flag
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # Auto-Extract Pincode Logic
    def save(self, *args, **kwargs):
        # Look for a 6-digit number in the location string
        match = re.search(r'\b\d{6}\b', self.location)
        if match:
            self.pincode = match.group()
        
        # Auto-update status based on is_available
        if not self.is_available:
            if self.transaction_type == 'rent':
                self.status = 'LENDED'
            else:
                self.status = 'SOLD'
                
        super().save(*args, **kwargs)

# --- 2. REVIEW MODEL (Restored) ---
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()

# --- 3. CART MODEL (Restored) ---
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)

# --- 4. USER PROFILE MODEL (Restored) ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, default='images/default.png') 

    def __str__(self):
        return self.user.username
    
# --- 5. USER CREDIT MODEL (Restored) ---
class UserCredit(models.Model):
    giver = models.ForeignKey(User, related_name='credits_given', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='credits_received', on_delete=models.CASCADE)
    score = models.IntegerField(default=1) 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username}"
    
# --- 6. ORDER MODEL (Restored) ---
class Order(models.Model):
    buyer = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.book.title} from {self.seller.username}"