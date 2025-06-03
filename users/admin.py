from django.contrib import admin
from BookStore.models import Chat, ChatParticipant, Message, Notification, User, Listing, City, Category, Tag, Role, UserRole, ListingTags, Image, Wishlist, WishlistCategories, WishlistTags, Review, Complaint

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


# Inline для участников чата
class ChatParticipantInline(admin.TabularInline):
    model = ChatParticipant
    extra = 0
    readonly_fields = ('user',)
    can_delete = False

# Inline для сообщений в чате
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'sent_at', 'is_read')
    can_delete = False

# Inline для уведомлений
class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
    readonly_fields = ('user', 'message', 'is_read', 'created_at')
    can_delete = False

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'created_at', 'get_participants')
    list_filter = ('created_at',)
    search_fields = ('listing__title',)
    readonly_fields = ('created_at',)
    inlines = [ChatParticipantInline, MessageInline]

    def get_participants(self, obj):
        return ", ".join([p.user.username for p in obj.chatparticipant_set.all()])
    get_participants.short_description = 'Participants'

@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user')
    list_filter = ('chat',)
    search_fields = ('user__username', 'chat__id')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'text_preview', 'sent_at', 'is_read')
    list_filter = ('sent_at', 'is_read')
    search_fields = ('text', 'sender__username', 'chat__id')
    readonly_fields = ('chat', 'sender', 'text', 'sent_at', 'is_read')
    inlines = [NotificationInline]

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__text')
    readonly_fields = ('user', 'message', 'is_read', 'created_at')