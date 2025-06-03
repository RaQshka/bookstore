from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WishlistForm
from BookStore.models import Wishlist, Category, Tag, City
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WishlistForm
from BookStore.models import Wishlist, Category, Tag, City

@login_required
def add_from_search(request):
    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.user = request.user
            wishlist.save()
            form.save_m2m()  # Сохраняем ManyToMany-поля
            return redirect('wishlist:list')
    else:
        # Подготовка начальных данных из GET-параметров
        initial_data = {
            'title': request.GET.get('title'),
            'author': request.GET.get('author'),
            'language': request.GET.get('language'),
            'min_condition': request.GET.get('condition'),
            'price_min': request.GET.get('price_min'),
            'price_max': request.GET.get('price_max'),
            'series': request.GET.get('series'),
            'number_of_pages': request.GET.get('number_of_pages'),
            'isbn': request.GET.get('isbn'),
            'dimensions': request.GET.get('dimensions'),
            'publisher': request.GET.get('publisher'),
            'cover_type': request.GET.get('cover_type'),
            'year': request.GET.get('year'),
            'illustrations_type': request.GET.get('illustrations_type'),
            'description': request.GET.get('description'),
            'is_exchange': True if request.GET.get('is_exchange') == '1' else False if request.GET.get('is_exchange') == '0' else None,
            'exchange_conditions': request.GET.get('exchange_conditions'),
        }

        # Обработка параметра city
        city_id = request.GET.get('city')
        if city_id and city_id.isdigit():
            initial_data['city'] = City.objects.filter(id=int(city_id)).first()
        else:
            initial_data['city'] = None

        # Обработка категорий
        category_ids = [int(cat_id) for cat_id in request.GET.getlist('category') if cat_id.isdigit()]
        if category_ids:
            initial_data['categories'] = Category.objects.filter(id__in=category_ids)
        else:
            initial_data['categories'] = None

        # Обработка тегов
        tag_ids = [int(tag_id) for tag_id in request.GET.getlist('tags') if tag_id.isdigit()]
        if tag_ids:
            initial_data['tags'] = Tag.objects.filter(id__in=tag_ids)
        else:
            initial_data['tags'] = None

        form = WishlistForm(initial=initial_data)
    return render(request, 'wishlist/create.html', {'form': form})
@login_required
def wishlist_list(request):
    wishlists = Wishlist.objects.filter(user=request.user).prefetch_related('wishlistcategories_set__category', 'tag_links__tag')
    return render(request, 'wishlist/list.html', {'wishlists': wishlists})
@login_required
def edit_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist)
        if form.is_valid():
            form.save()
            return redirect('wishlist:list')
    else:
        form = WishlistForm(instance=wishlist)
    return render(request, 'wishlist/edit.html', {'form': form, 'wishlist': wishlist})

@login_required
def delete_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    if request.method == 'POST':
        wishlist.delete()
        return redirect('wishlist:list')
    return render(request, 'wishlist/delete.html', {'wishlist': wishlist})