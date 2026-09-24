"""
Database models for auction items, bids, messages,
and user-related data used in the application.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class PageView(models.Model):
    """
    Model to track page views
    
    Defines a simple model with a count field to track the number of page views.
    """
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    
    Adds additional fields: email, date of birth (dob), and profile image.
    """

    email = models.EmailField(unique=True, verbose_name='Email Address')
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        null=True, 
        blank=True,
        verbose_name='Profile Picture' # Django Admin Interface label
    )
        
    # Using email for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Item(models.Model):
    """
    Model representing an auction item

    Includes fields for the user who listed the item, title, description,
    starting price, image, auction end time, and creation timestamp.
    """

    user = models.ForeignKey(
        'api.User',  # Custom user model 
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))] 
    )
    
    # Auction item image
    image = models.ImageField(
        upload_to='item_images/',
        blank=True,
        null=True,
    )
    
    # Auction end date/time
    auction_end = models.DateTimeField()
    
    # Automatically track creation time
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - £{self.starting_price}"
    
class Bid(models.Model):
    """
    Model representing a bid on an auction item

    Includes fields for the item being bid on, the user placing the bid,
    bid amount, creation timestamp, and bid status.
    """

    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='bids'
    )

    user = models.ForeignKey(
        'api.User',   # Custom user model 
        on_delete=models.CASCADE,
        related_name='bids'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),      # Current highest bid
        ('OUTBID', 'Outbid'),        # Someone bid higher
        ('WON', 'Won'),              # Won auction
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    class Meta:
        ordering = ['-amount']  # Highest bid first
        unique_together = ['item', 'user', 'amount']  # Prevent duplicate bids
    
    def __str__(self) -> str:
        return f"${self.amount} on {self.item.title} by {self.user.username}"
    
class Question(models.Model):
    """
    Model representing a question about an auction item

    Includes fields for the item, user who asked, question text,
    answer text, creation timestamp, and answered timestamp.
    """
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    answer = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_answered(self):
        return bool(self.answer)
    
    def __str__(self):
        return f"{self.text}"
