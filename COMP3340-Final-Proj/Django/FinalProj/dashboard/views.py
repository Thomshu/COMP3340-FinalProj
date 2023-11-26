from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import Item
from django.core.paginator import Paginator

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
    return render(request, 'dashboard/cart.html')