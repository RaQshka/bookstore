from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Валидатор для ограничения размера изображения
def validate_image_size(value):
    max_size = 3 * 1024 * 1024  # 3 МБ в байтах
    if value.size > max_size:
        raise ValidationError('Размер изображения не должен превышать 3 МБ.')

# Модель City (Города)
class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'City'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

# Модель Category (Категории)
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

# Модель Tag (Теги)
class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

# Модель Role (Роли)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Role'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name

# Модель User (Пользователи)
class User(AbstractUser):
    first_name = models.CharField(max_length=30)  # Имя
    last_name = models.CharField(max_length=30)   # Фамилия
    patronymic = models.CharField(max_length=30, null=True, blank=True)  # Отчество
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Номер телефона
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, validators=[validate_image_size])  # Аватар
    description = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'User'
        indexes = [models.Index(fields=['email'])]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def rating(self):
        reviews = self.reviews_received.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 2)
        return None

# Модель UserRole (Роли пользователей)
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserRole'
        unique_together = ('user', 'role')
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

# Модель Listing (Объявления)
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    series = models.CharField(max_length=100, null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_type = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    illustrations_type = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_exchange = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, through='ListingTags')
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('like_new', 'Почти новое'),
        ('good', 'Хорошее'),
        ('fair', 'Посредственное'),
        ('poor', 'Плохое'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    MODERATION_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Подтверждено'),
        ('rejected', 'Отказано'),
    ]
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Активное'),
        ('sold', 'Продано'),
        ('exchanged', 'Exchanged'),
        ('deleted', 'Удалено'),

    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    exchange_conditions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Listing'
        indexes = [models.Index(fields=['seller']), models.Index(fields=['status'])]
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f"{self.title} by {self.author}"

# Модель Listing_Tags (Теги объявлений)
class ListingTags(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Listing_Tags'
        unique_together = ('listing', 'tag')
        verbose_name = 'Тег объявления'
        verbose_name_plural = 'Теги объявлений'

    def __str__(self):
        return f"{self.listing.title} - {self.tag.name}"

# Модель Image (Изображения)
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/', null=True, blank=True, validators=[validate_image_size])

    class Meta:
        db_table = 'ListingImage'
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'

    def __str__(self):
        return f"Image for {self.listing.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    MIN_CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('like_new', 'Почти новое'),
        ('good', 'Хорошее'),
        ('fair', 'Посредственное'),
        ('poor', 'Плохое'),
    ]
    min_condition = models.CharField(max_length=20, choices=MIN_CONDITION_CHOICES, null=True, blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    series = models.CharField(max_length=100, null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_type = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    illustrations_type = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_exchange = models.BooleanField(null=True, blank=True)
    exchange_conditions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Wishlist'
        indexes = [models.Index(fields=['user'])]
        verbose_name = 'Список желаемого'
        verbose_name_plural = 'Списки желаемого'

    def __str__(self):
        return f"{self.user.username}'s wishlist"

# Модель Wishlist_Categories (Категории желаемого)
class WishlistCategories(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_links')

    class Meta:
        db_table = 'Wishlist_Categories'
        unique_together = ('wishlist', 'category')
        verbose_name = 'Категория желаемого'
        verbose_name_plural = 'Категории желаемого'

    def __str__(self):
        return f"{self.wishlist} - {self.category.name}"

# Модель Wishlist_Tags (Теги желаемого)
class WishlistTags(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='tag_links')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Wishlist_Tags'
        unique_together = ('wishlist', 'tag')
        verbose_name = 'Тег желаемого'
        verbose_name_plural = 'Теги желаемого'

    def __str__(self):
        return f"{self.wishlist} - {self.tag.name}"

# Модель Chat (Чаты)
class Chat(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Chat'
        indexes = [models.Index(fields=['listing'])]
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f"Chat {self.id}"

# Модель ChatParticipant (Участники чата)
class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ChatParticipant'
        unique_together = ('chat', 'user')
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чата'

    def __str__(self):
        return f"{self.user.username} in Chat {self.chat.id}"

# Модель Message (Сообщения)
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Изменено на CASCADE
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Message'
        indexes = [models.Index(fields=['chat']), models.Index(fields=['sender'])]
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"Message from {self.sender.username}"

# Модель Review (Отзывы)
class Review(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')  # О ком отзыв
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')  # Кто оставил отзыв
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)  # Необязательное поле
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Review'
        indexes = [models.Index(fields=['to_user'])]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Review by {self.from_user.username} for {self.to_user.username}"

# Модель Complaint (Жалобы)
class Complaint(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_reported')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_received', null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Complaint'
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        target = self.target_user.username if self.target_user else f"Listing {self.listing.id}"
        return f"Complaint by {self.reporter.username} on {target}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name='notifications',null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Notification'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        if self.message:
            return f"Уведомление для {self.user.username} о сообщении {self.message.id}"
        elif self.listing:
            return f"Уведомление для {self.user.username} о новом объявлении {self.listing.id}"
        else:
            return f"Уведомление для {self.user.username}"