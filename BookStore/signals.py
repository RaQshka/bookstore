from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Listing, Wishlist, Notification, User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Listing)
def check_wishlists_on_approval(sender, instance, **kwargs):
    if instance.moderation_status == 'approved' and not instance._state.adding:
        # Используем правильные пути для предзагрузки связанных объектов
        wishlists = Wishlist.objects.all().select_related('user', 'city').prefetch_related(
            'wishlistcategories_set__category',
            'tag_links__tag'
        )
        channel_layer = get_channel_layer()
        for wishlist in wishlists:
            if matches_wishlist(instance, wishlist):
                # Создаём уведомление
                notification = Notification.objects.create(
                    user=wishlist.user,
                    listing=instance,
                    is_read=False
                )
                # Отправляем уведомление через WebSocket
                notification_data = {
                    'type': 'send_notification',  # Соответствует методу в NotificationConsumer
                    'notification': {
                        'id': notification.id,
                        'listing_id': instance.id,
                        'listing_title': instance.title,
                        'message': f"Новое объявление '{instance.title}' соответствует вашему списку желаемого!",
                        'created_at': notification.created_at.isoformat(),
                        'is_read': notification.is_read
                    }
                }
                async_to_sync(channel_layer.group_send)(
                    f'user_{wishlist.user.id}',
                    notification_data
                )

def matches_wishlist(listing, wishlist):
    # Проверка по названию
    if wishlist.title and wishlist.title.lower() not in listing.title.lower():
        return False

    # Проверка по автору
    if wishlist.author and wishlist.author.lower() not in listing.author.lower():
        return False

    # Проверка по языку
    if wishlist.language and wishlist.language.lower() != listing.language.lower():
        return False

    # Проверка по минимальному состоянию
    if wishlist.min_condition:
        condition_order = {'new': 5, 'like_new': 4, 'good': 3, 'fair': 2, 'poor': 1}
        if condition_order.get(listing.condition, 0) < condition_order.get(wishlist.min_condition, 0):
            return False

    # Проверка по диапазону цены
    if wishlist.price_min is not None and listing.price is not None and listing.price < wishlist.price_min:
        return False
    if wishlist.price_max is not None and listing.price is not None and listing.price > wishlist.price_max:
        return False

    # Проверка по городу
    if wishlist.city and listing.seller.city != wishlist.city:
        return False

    # Проверка по категории
    wishlist_categories = [wc.category.id for wc in wishlist.wishlistcategories_set.all()]  # Исправлено с category_links на wishlistcategories_set
    if wishlist_categories and listing.category_id not in wishlist_categories:
        return False

    # Проверка по тегам
    wishlist_tags = [wt.tag.id for wt in wishlist.tag_links.all()]  # Остаётся без изменений
    listing_tags = listing.tags.all().values_list('id', flat=True)
    if wishlist_tags and not set(wishlist_tags).issubset(set(listing_tags)):
        return False

    # Проверка по серии
    if wishlist.series and wishlist.series.lower() not in (listing.series.lower() if listing.series else ""):
        return False

    # Проверка по количеству страниц
    if wishlist.number_of_pages is not None and listing.number_of_pages != wishlist.number_of_pages:
        return False

    # Проверка по ISBN
    if wishlist.isbn and wishlist.isbn != (listing.isbn or ""):
        return False

    # Проверка по размерам
    if wishlist.dimensions and wishlist.dimensions.lower() != (listing.dimensions.lower() if listing.dimensions else ""):
        return False

    # Проверка по издателю
    if wishlist.publisher and wishlist.publisher.lower() != (listing.publisher.lower() if listing.publisher else ""):
        return False

    # Проверка по типу обложки
    if wishlist.cover_type and wishlist.cover_type.lower() != (listing.cover_type.lower() if listing.cover_type else ""):
        return False

    # Проверка по году
    if wishlist.year is not None and listing.year != wishlist.year:
        return False

    # Проверка по типу иллюстраций
    if wishlist.illustrations_type and wishlist.illustrations_type.lower() != (listing.illustrations_type.lower() if listing.illustrations_type else ""):
        return False

    # Проверка по описанию
    if wishlist.description and wishlist.description.lower() not in (listing.description.lower() if listing.description else ""):
        return False

    # Проверка по обмену
    if wishlist.is_exchange is not None and listing.is_exchange != wishlist.is_exchange:
        return False

    # Проверка по условиям обмена
    if wishlist.exchange_conditions and wishlist.exchange_conditions.lower() not in (listing.exchange_conditions.lower() if listing.exchange_conditions else ""):
        return False

    return True