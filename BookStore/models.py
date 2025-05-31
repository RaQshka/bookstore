from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель City (Города)
class City(models.Model):
    name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'City'

    def __str__(self):
        return self.name

# Модель Category (Категории)
class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.name

# Модель Tag (Теги)
class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'Tag'

    def __str__(self):
        return self.name

# Модель Role (Роли)
class Role(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.name

# Модель User (Пользователи)
class User(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)  # Имя
    last_name = models.CharField(max_length=30, null=False)   # Фамилия
    patronymic = models.CharField(max_length=30, null=True, blank=True)  # Отчество
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Номер телефона
    email = models.EmailField(unique=True, null=False)
    avatar_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    USERNAME_FIELD = 'email'  # Используем email для логина
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Обновлено: добавлены first_name и last_name как обязательные

    class Meta:
        db_table = 'User'
        indexes = [models.Index(fields=['email'])]

    def __str__(self):
        return self.email

# Модель UserRole (Роли пользователей)
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'UserRole'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"

# Модель Listing (Объявления)
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=100, null=False)
    series = models.CharField(max_length=100, null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_type = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    illustrations_type = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_exchange = models.BooleanField(default=False)
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    MODERATION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES, null=False)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('exchanged', 'Exchanged'),
        ('deleted', 'Deleted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False)
    exchange_conditions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Listing'
        indexes = [models.Index(fields=['seller']), models.Index(fields=['status'])]

    def __str__(self):
        return f"{self.title} by {self.author}"

# Модель Listing_Tags (Теги объявлений)
class ListingTags(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'Listing_Tags'
        unique_together = ('listing', 'tag')

    def __str__(self):
        return f"{self.listing.title} - {self.tag.name}"

# Модель Image (Изображения)
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False)
    image_url = models.URLField(null=False)

    class Meta:
        db_table = 'Image'

    def __str__(self):
        return self.image_url

# Модель Wishlist (Список желаемого)
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    MIN_CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    min_condition = models.CharField(max_length=20, choices=MIN_CONDITION_CHOICES, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Wishlist'
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f"{self.user.username}'s wishlist"

# Модель Wishlist_Categories (Категории желаемого)
class WishlistCategories(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'Wishlist_Categories'
        unique_together = ('wishlist', 'category')

    def __str__(self):
        return f"{self.wishlist} - {self.category.name}"

# Модель Wishlist_Tags (Теги желаемого)
class WishlistTags(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'Wishlist_Tags'
        unique_together = ('wishlist', 'tag')

    def __str__(self):
        return f"{self.wishlist} - {self.tag.name}"

# Модель Chat (Чаты)
class Chat(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Chat'
        indexes = [models.Index(fields=['listing'])]

    def __str__(self):
        return f"Chat {self.id}"  # Исправлено: chatid не существует, используем id

# Модель ChatParticipant (Участники чата)
class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'ChatParticipant'
        unique_together = ('chat', 'user')

    def __str__(self):
        return f"{self.user.username} in Chat {self.chat.id}"

# Модель Message (Сообщения)
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    text = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True, null=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Message'
        indexes = [models.Index(fields=['chat']), models.Index(fields=['sender'])]

    def __str__(self):
        return f"Message from {self.sender.username}"

# Модель Review (Отзывы)
class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=False)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Review'
        indexes = [models.Index(fields=['listing'])]

    def __str__(self):
        return f"Review by {self.user.username} for {self.listing.title}"

# Модель Complaint (Жалобы)
class Complaint(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='complaints_reported')
    target_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='complaints_received')  # Исправлено на target_user
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, null=True, blank=True)
    message = models.TextField(null=False)
    reason = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'Complaint'

    def __str__(self):
        return f"Complaint by {self.reporter.username} on {self.target_user.username}"