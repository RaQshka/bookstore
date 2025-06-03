from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from BookStore.models import User, Listing, Complaint

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.reporter = request.user

            target_user_id = request.POST.get('target_user_id')
            listing_id = request.POST.get('listing_id')

            if not target_user_id and not listing_id:
                form.add_error(None, "Не указан объект жалобы.")
                return render(request, 'complaints/submit_complaint.html', {'form': form})

            # Проверка на существующую жалобу
            if target_user_id:
                if Complaint.objects.filter(reporter=request.user, target_user_id=target_user_id).exists():
                    return redirect(request.META.get('HTTP_REFERER', '/'))  # Уже есть жалоба на этого пользователя
                complaint.target_user = get_object_or_404(User, id=target_user_id)
            elif listing_id:
                if Complaint.objects.filter(reporter=request.user, listing_id=listing_id).exists():
                    return redirect(request.META.get('HTTP_REFERER', '/'))  # Уже есть жалоба на это объявление
                listing = get_object_or_404(Listing, id=listing_id)
                complaint.listing = listing
                complaint.target_user = listing.seller  # Связь с продавцом для ясности в админке

            complaint.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ComplaintForm()

    return render(request, 'complaints/submit_complaint.html', {'form': form})