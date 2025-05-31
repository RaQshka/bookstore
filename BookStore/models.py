from django.db import models

# Модель для таблицы City
class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'City'

# Модель для таблицы Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'

# Модель для таблицы Tag
class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Tag'

# Модель для таблицы Role
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Role'

# Модель для таблицы User
class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)

    class Meta:
        db_table = 'User'

# Модель для таблицы UserRole
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserRole'
        unique_together = ('user', 'role')

# Модель для таблицы Book
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    series = models.CharField(max_length=100, null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True, unique=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_type = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    illustrations_type = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Book'

# Модель для таблицы Book_Tags
class BookTags(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Book_Tags'
        unique_together = ('book', 'tag')

# Модель для таблицы Listing
class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    MODERATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('exchanged', 'Exchanged'),
        ('deleted', 'Deleted'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posti_exchange = models.BooleanField(default=False)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    moderation_status = models.CharField(max_length=20, choices=MODERATION_STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    exchange_conditions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Listing'

# Модель для таблицы Listing_Tags
class ListingTags(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Listing_Tags'
        unique_together = ('listing', 'tag')

# Модель для таблицы Image
class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=255)

    class Meta:
        db_table = 'Image'

# Модель для таблицы Wishlist
class Wishlist(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    min_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'Wishlist'

# Модель для таблицы Wishlist_Categories
class WishlistCategories(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Wishlist_Categories'
        unique_together = ('wishlist', 'category')

# Модель для таблицы Wishlist_Tags
class WishlistTags(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Wishlist_Tags'
        unique_together = ('wishlist', 'tag')

# Модель для таблицы Chat
class Chat(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Chat'

# Модель для таблицы ChatParticipant
class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ChatParticipant'
        unique_together = ('chat', 'user')

# Модель для таблицы Message
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Message'

# Модель для таблицы Review
class Review(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Review'

# Модель для таблицы Complaint
class Complaint(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_complaints')
    target_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='targeted_complaints')
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, null=True, blank=True)
    message = models.TextField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Complaint'