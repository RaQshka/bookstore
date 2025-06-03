from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from BookStore.models import Listing, Chat, ChatParticipant, Message, Notification

@login_required
def start_chat(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.seller:
        return redirect('listings:detail', pk=listing.pk)

    chat = Chat.objects.filter(
        listing=listing,
        chatparticipant__user__in=[request.user, listing.seller]
    ).distinct().first()

    if not chat:
        chat = Chat.objects.create(listing=listing)
        ChatParticipant.objects.create(chat=chat, user=request.user)
        ChatParticipant.objects.create(chat=chat, user=listing.seller)

    return redirect('chat:chat_detail', chat_id=chat.id)

@login_required
def chat_list(request):
    chats = Chat.objects.filter(chatparticipant__user=request.user).order_by('-created_at')
    return render(request, 'chat/chat_list.html', {'chats': chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id, chatparticipant__user=request.user)
    messages = Message.objects.filter(chat=chat).order_by('sent_at')
    Notification.objects.filter(user=request.user, message__chat=chat).update(is_read=True)
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return render(request, 'chat/notifications.html', {'notifications': notifications})