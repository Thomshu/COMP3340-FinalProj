from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse

from item.models import Item
from django.core.paginator import Paginator
from django.http import HttpResponse

# This is for clicking on the dashboard button and displaying the items that the User has added
@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    p = Paginator(items, 6)
    page = request.GET.get('page')
    items_list = p.get_page(page)

    numPages = "a" * items_list.paginator.num_pages

    return render(request, 'dashboard/index.html', {
        'items': items_list,
        'numPages': numPages
    })

def cart(request):
    cart_items = request.session.get('cart', [])
    
    sub_total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    tax = sub_total_price*0.13
    total = sub_total_price+tax

    return render(request, 'dashboard/cart.html', {'cart_items': cart_items, 'sub_total': sub_total_price, 'tax': tax, 'total': total})

def add_to_cart(request, item_id):
    # Get the item
    item = get_object_or_404(Item, id=item_id)

    # Get the user's cart from the session
    cart = request.session.get('cart', [])

    # Check if the item is already in the cart
    item_in_cart = next((cart_item for cart_item in cart if cart_item['id'] == item.id), None)

    if item_in_cart:
        # If the item is already in the cart, update the quantity
        item_in_cart['quantity'] += 1
        item_in_cart['total'] = item_in_cart['quantity'] * item.price
    else:
        # If the item is not in the cart, add it with a default quantity of 1
        cart_item = {
            'id': item.id,
            'image': item.image.url,  # Add the image URL
            'name': item.name,
            'price': item.price,
            'quantity': 1,
            'total': item.price * 1,  # Initial total calculation
        }

        cart.append(cart_item)

    # Update the session with the modified cart
    request.session['cart'] = cart

    # Redirect to the cart page
    return redirect(reverse('dashboard:cart'))

def remove_from_cart(request, item_id):
    # Get the user's cart from the session
    cart = request.session.get('cart', [])

    # Check if the item is in the cart
    cart_item = next((item for item in cart if item['id'] == item_id), None)

    if cart_item:
        # If the item is in the cart, remove it
        cart.remove(cart_item)
        request.session['cart'] = cart

    # Redirect back to the cart page
    return redirect(reverse('dashboard:cart'))
