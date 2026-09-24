"""
Admin configuration for managing auction items, bids,
users, and related models through the Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Item, Bid, Question
from django.utils.html import format_html

# Unregister if already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the User model
    
    Defines the admin interface for the custom User model, including
    fieldsets, list display, filters, and custom methods for displaying
    date of birth and profile image preview.
    """

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'dob', 'profile_image', 'profile_image_preview')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # New user fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'dob', 'profile_image'),
        }),
    )
    
    # List view display
    list_display = ('email', 'username', 'first_name', 'last_name', 'get_dob', 'profile_image_preview', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('profile_image_preview',)
    
    # Custom method to display DOB
    def get_dob(self, obj):
        return obj.dob.strftime('%Y-%m-%d') if obj.dob else "-"
    get_dob.short_description = 'Date of Birth'
    get_dob.admin_order_field = 'dob'
    
    # Custom method to display profile image preview
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image.url)
        return "Image not found"

    # view profile image
    def view_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.profile_image.url))
        return "Image not found"
    

class ItemAdmin(admin.ModelAdmin):
    """
    Custom admin for the Item model
    
    Defines the admin interface for the Item model, including
    list display and custom methods for displaying starting price
    and image preview.
    """
    
    list_display = ('id', 'title', 'user', 'formatted_starting_price', 'auction_end', 'created_at', 'image_preview')

    def image_preview(self, obj):
        """
        Display a small preview of the item's image in the admin interface
        
        Args:
            obj (Item): The Item instance
        """
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50;" />', obj.image.url)
        return "No image"
    
    def formatted_starting_price(self, obj):
        return f"£{obj.starting_price}"
    formatted_starting_price.short_description = 'Starting Price' 

    image_preview.short_description = 'Item Image' 

# Unregister if already registered
try:
    admin.site.unregister(Item)
except admin.sites.NotRegistered:
    pass 

# Register the Item model again
admin.site.register(Item, ItemAdmin)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """
    Custom admin for the Bid model
    
    Defines the admin interface for the Bid model, including
    list display, filters, search fields, and ordering.
    """
    
    list_display = ('id', 'item', 'user', 'status', 'amount', 'created_at')
    list_filter = ('item', 'user', 'status', 'created_at')
    search_fields = ('item__title', 'user__username', 'amount')
    ordering = ('-created_at',)

@admin.register(Question)
class BidAdmin(admin.ModelAdmin):
    """
    Custom admin for the Question model
    
    Defines the admin interface for the Question model, including
    list display, filters, and ordering.
    """
    
    list_display = ('id', 'item', 'user', 'text', 'answer', 'created_at', 'answered_at')
    list_filter = ('created_at', 'item', 'user', 'answered_at')
    ordering = ('-created_at',)