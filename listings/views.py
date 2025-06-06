from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from BookStore.models import Listing, Image, Category, Tag, City
from .forms import ListingForm

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.moderation_status = 'pending'
            listing.status = 'active'
            listing.save()
            form.save_m2m()  # Сохраняем теги
            if 'image' in request.FILES:
                Image.objects.create(listing=listing, image=request.FILES['image'])
            return redirect('listings:list')
    else:
        form = ListingForm()
    categories = Category.objects.all()  # Добавляем категории
    return render(request, 'listings/create.html', {'form': form, 'categories': categories})

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            if 'image' in request.FILES:
                Image.objects.create(listing=listing, image=request.FILES['image'])
            return redirect('listings:detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/edit.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.status = 'deleted'
        listing.save()
        return redirect('listings:list')
    return render(request, 'listings/delete.html', {'listing': listing})

def listing_list(request):
    listings = Listing.objects.filter(status='active', moderation_status='approved')

    # Получаем параметры из GET-запроса
    search = request.GET.get('search')
    category = request.GET.get('category')
    tags = request.GET.getlist('tags')
    city = request.GET.get('city')
    title = request.GET.get('title')
    author = request.GET.get('author')
    language = request.GET.get('language')
    condition = request.GET.get('condition')
    series = request.GET.get('series')
    number_of_pages = request.GET.get('number_of_pages')
    isbn = request.GET.get('isbn')
    dimensions = request.GET.get('dimensions')
    publisher = request.GET.get('publisher')
    cover_type = request.GET.get('cover_type')
    year = request.GET.get('year')
    illustrations_type = request.GET.get('illustrations_type')
    description = request.GET.get('description')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    is_exchange = request.GET.get('is_exchange')
    exchange_conditions = request.GET.get('exchange_conditions')

    # Фильтрация по поиску
    if search:
        listings = listings.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    # Фильтрация по категории
    if category:
        listings = listings.filter(category_id=category)

    # Фильтрация по тегам
    if tags:
        for tag in tags:
            listings = listings.filter(tags__id=tag)

    # Фильтрация по городу
    if city:
        listings = listings.filter(seller__city_id=city)

    # Фильтрация по обязательным полям
    if title:
        listings = listings.filter(title__icontains=title)
    if author:
        listings = listings.filter(author__icontains=author)
    if language:
        listings = listings.filter(language__icontains=language)
    if condition:
        listings = listings.filter(condition=condition)

    # Фильтрация по необязательным полям
    if series:
        listings = listings.filter(series__icontains=series)
    if number_of_pages:
        listings = listings.filter(number_of_pages=number_of_pages)
    if isbn:
        listings = listings.filter(isbn__icontains=isbn)
    if dimensions:
        listings = listings.filter(dimensions__icontains=dimensions)
    if publisher:
        listings = listings.filter(publisher__icontains=publisher)
    if cover_type:
        listings = listings.filter(cover_type__icontains=cover_type)
    if year:
        listings = listings.filter(year=year)
    if illustrations_type:
        listings = listings.filter(illustrations_type__icontains=illustrations_type)
    if description:
        listings = listings.filter(description__icontains=description)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if is_exchange:
        listings = listings.filter(is_exchange=is_exchange == '1')
    if exchange_conditions:
        listings = listings.filter(exchange_conditions__icontains=exchange_conditions)

    # Данные для шаблона
    categories = Category.objects.all()
    tags = Tag.objects.all()
    cities = City.objects.all()
    condition_choices = Listing.CONDITION_CHOICES
    selected_tags = request.GET.getlist('tags')

    return render(request, 'listings/list.html', {
        'listings': listings,
        'categories': categories,
        'tags': tags,
        'cities': cities,
        'selected_tags': selected_tags,
        'condition_choices': condition_choices,
    })
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status='active', moderation_status='approved')
    return render(request, 'listings/detail.html', {'listing': listing})