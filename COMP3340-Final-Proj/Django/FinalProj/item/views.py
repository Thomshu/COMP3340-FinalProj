from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def browse(request):
    query = request.GET.get('query', '')  # Backend query part
    selected_categories = request.GET.getlist('category')  # Get a list of selected categories
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if selected_categories:
        items = items.filter(category__in=selected_categories)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    p = Paginator(items, 9)
    page = request.GET.get('page')
    items_list = p.get_page(page)
    numPages = "a" * items_list.paginator.num_pages

    if is_ajax(request=request):  # Check if it's an AJAX request
            # Render the item list as HTML
            html_content = render_to_string('item/item_list.html', {'items': items_list})
            return JsonResponse({'html_content': html_content, 'numPages': numPages})

    return render(request, 'item/browse.html', {
        'items': items_list,
        'numPages': numPages,
        'query': query,
        'categories': categories,
        'selected_categories': selected_categories
    })

# This view is for creating the details page for the item
def detail(request, pk): #pk stands for primary key
    item = get_object_or_404(Item, pk=pk) #Get the object, or get 404 error
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3] #this is for displaying related items in the same category

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

#Making it a requirement that we have to be logged in first, in order to add items, if not logged in and we try to add an item, redirected to login page instead
@login_required
def new(request):
    if request.method == 'POST': #this is if the form is submitted
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else: #Aka if its a get request
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Add New Item', #for forms.html
    })

#This is for deleting items
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index') #after deleting return to dashboard

# This is for editting items, similar to new() above, but adjusted slightly
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST': #this is if the form is submitted
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save() #This is adjusted to be simply as we know for sure it's already created, so we simply need to save() now

            return redirect('item:detail', pk=item.id)
    else: #Aka if its a get request
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item', 
    })