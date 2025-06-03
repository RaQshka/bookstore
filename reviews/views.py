from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from BookStore.models import Listing, Review

@login_required
def submit_review(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.seller:
        return redirect('listings:detail', listing.pk)  # Нельзя оставить отзыв на свое объявление

    # Проверка, оставил ли пользователь уже отзыв
    if Review.objects.filter(from_user=request.user, listing=listing).exists():
        return redirect('listings:detail', listing.pk)  # Один отзыв на объявление

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.to_user = listing.seller
            review.from_user = request.user
            review.listing = listing
            review.save()
            return redirect('listings:detail', pk=listing_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form, 'listing': listing})