from django.contrib import admin
from BookStore.models import User, City, Listing, Image, Category, Tag

# Register City model
admin.site.register(City)

# Customize User model in admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'city', 'is_banned')
    search_fields = ('username', 'email')
    list_filter = ('is_banned', 'city')
    fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone_number', 'city', 'avatar', 'description', 'is_banned', 'is_superuser', 'is_staff')

admin.site.register(User, UserAdmin)

# Customize Listing model and admin interface
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'status', 'moderation_status', 'created_at')
    search_fields = ('title', 'seller__username')
    list_filter = ('status', 'moderation_status', 'category')
    actions = ['approve_listings', 'reject_listings']

    def approve_listings(self, request, queryset):
        queryset.update(moderation_status='approved')
    approve_listings.short_description = "Approve selected listings"

    def reject_listings(self, request, queryset):
        queryset.update(moderation_status='rejected')
    reject_listings.short_description = "Reject selected listings"

admin.site.register(Listing, ListingAdmin)

# Register other models
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Tag)