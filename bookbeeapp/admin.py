from django.contrib import admin
from .models import Book, Review, Cart, UserProfile, UserCredit, Order

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(UserProfile)
admin.site.register(UserCredit)
admin.site.register(Order)