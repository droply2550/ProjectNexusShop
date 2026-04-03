from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Card
from .forms import CardForm


def home(request):
    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(name__icontains=query)
    else:
        cards = Card.objects.all()
    return render(request, 'index.html', {'cards': cards})


def product_list(request):
    cards = Card.objects.all()

    q = request.GET.get('q')
    if q:
        cards = cards.filter(name__icontains=q)

    selected_rarities = request.GET.getlist('rarity')
    if selected_rarities:
        cards = cards.filter(rarity__in=selected_rarities)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        cards = cards.order_by('price')
    elif sort == 'price_desc':
        cards = cards.order_by('-price')
    elif sort == 'name_asc':
        cards = cards.order_by('name')
    elif sort == 'name_desc':
        cards = cards.order_by('-name')

    page_size = 8
    paginator = Paginator(cards, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rarities = ['RRR', 'RR', 'SP', 'R', 'BT']
    result = {
        'cards': page_obj,
        'rarities': rarities,
        'selected_rarities': selected_rarities,
        'search_query': q or '',
        'sort': sort or '',
        'page_obj': page_obj,
        'cart_total_items': get_cart_count(request),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for card in page_obj:
            data.append({
                'id': card.pk,
                'name': card.name,
                'series': card.series,
                'price': str(card.price),
                'rarity': card.rarity,
                'stock': card.stock,
                'image': card.image.url if card.image else None,
            })
        return JsonResponse({'cards': data, 'count': paginator.count}, safe=False)

    return render(request, 'products.html', result)


def get_cart_count(request):
    cart = request.session.get('cart', {})
    return sum(int(item.get('qty', 0)) for item in cart.values())


def product_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, 'product-detail.html', {'card': card, 'cart_total_items': get_cart_count(request)})


def about(request):
    return render(request, 'about.html', {'cart_total_items': get_cart_count(request)})


def contact(request):
    return render(request, 'contact.html', {'cart_total_items': get_cart_count(request)})


def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0
    for key, item in cart_data.items():
        subtotal = float(item.get('price', 0)) * int(item.get('qty', 0))
        total += subtotal
        cart_items.append({
            'id': key,
            'name': item.get('name'),
            'price': item.get('price'),
            'qty': item.get('qty'),
            'image': item.get('image', ''),
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_total_items': get_cart_count(request),
    })


def card_edit(request, pk=None):
    if pk:
        card = get_object_or_404(Card, pk=pk)
    else:
        card = None

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = CardForm(instance=card)

    return render(request, 'card_form.html', {
        'form': form,
        'card': card,
        'cart_total_items': get_cart_count(request),
    })


def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        card.delete()
        return redirect('product_list')
    return render(request, 'card_confirm_delete.html', {
        'card': card,
        'cart_total_items': get_cart_count(request),
    })


def add_to_cart(request, pk):
    card = get_object_or_404(Card, pk=pk)
    cart = request.session.get('cart', {})
    key = str(pk)
    if key in cart:
        cart[key]['qty'] = int(cart[key]['qty']) + 1
    else:
        cart[key] = {
            'name': card.name,
            'price': str(card.price),
            'qty': 1,
            'image': card.image.url if card.image else '',
        }

    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'total_items': get_cart_count(request)})

    return redirect('cart')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
        success = True
    else:
        success = False
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_data = request.session.get('cart', {})
        total = sum(float(item.get('price', 0)) * int(item.get('qty', 0)) for item in cart_data.values())
        return JsonResponse({
            'success': success,
            'total_items': get_cart_count(request),
            'total': round(total, 2)
        })
    
    return redirect('cart')


def update_cart_quantity(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    cart = request.session.get('cart', {})
    key = str(pk)
    qty = request.POST.get('qty', 1)
    
    try:
        qty = int(qty)
        if qty < 0:
            qty = 0
    except ValueError:
        qty = 1
    
    if key in cart:
        if qty == 0:
            del cart[key]
        else:
            cart[key]['qty'] = qty
        request.session['cart'] = cart
        request.session.modified = True
        success = True
    else:
        success = False
    
    cart_data = request.session.get('cart', {})
    total = sum(float(item.get('price', 0)) * int(item.get('qty', 0)) for item in cart_data.values())
    
    return JsonResponse({
        'success': success,
        'total_items': get_cart_count(request),
        'total': round(total, 2)
    })