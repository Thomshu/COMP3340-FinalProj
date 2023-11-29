from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm, ImageForm
from .models import Category, Item, Images

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from django.forms import modelformset_factory
from django.template.loader import get_template

from django.contrib.auth.decorators import user_passes_test
import csv

def is_inventory_manager(user):
    return user.is_authenticated and user.is_inventoryManager

def browse(request):
    query = request.GET.get('query', '')
    selected_categories = request.GET.getlist('category')
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

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        # If the request is AJAX, render only the content of the item_list template
        template = get_template('item/item_list.html')
        html_content = template.render({'items': items_list})
        print("AJAX request. Returning JSON response.")
        return JsonResponse({'html_content': html_content, 'numPages': numPages})

    # If it's not an AJAX request, render the HTML page
    print("Non-AJAX request. Rendering HTML page.")
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
    images = item.images.all()  # Retrieve all images associated with the item

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):

    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=3, max_num=3) #'extra' means the number of photos that you can upload 
    if request.method == 'POST': #this is if the form is submitted
        form = NewItemForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(item=item, image=image)
                    photo.save()
            return redirect('item:detail', pk=item.id)
        else:
            print(form.errors, formset.errors)
    else: #Aka if its a get request
        form = NewItemForm()
        formset = ImageFormSet(queryset=Images.objects.none())

    # Create an instance of ImageForm to include in the context
    image_form = ImageForm()

    return render(request, 'item/form.html', {
        'form': form,
        'formset': formset,
        'image_form': image_form,  # Include the image form in the context
        'title': 'Add New Item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3, max_num=3)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.filter(item=item))

        if form.is_valid() and formset.is_valid():
            form.save()

            # Save only the last two forms in the formset
            for form_instance in formset[::-1][:2]:
                if form_instance.cleaned_data and not form_instance.cleaned_data.get('DELETE', False):
                    image = form_instance.cleaned_data['image']
                    photo = Images(item=item, image=image)
                    photo.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
        formset = ImageFormSet(queryset=Images.objects.filter(item=item))

    image_form = ImageForm()

    return render(request, 'item/form.html', {
        'form': form,
        'formset': formset,
        'image_form': image_form,
        'title': 'Edit Item',
    })

#This is for deleting items
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()

     # Redirect based on user role
    if is_inventory_manager(request.user):
        return redirect('dashboard:index')
    else:
        return redirect('item:browse')
    
def export_items_to_csv(request):
    # Get all items and related data
    items = Item.objects.all()

    # Create response object with appropriate CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items_export.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write CSV headers
    writer.writerow(['ID', 'Category', 'Name', 'Description', 'Price', 'Is Sold', 'Stock', 'Created By', 'Created At'])

    # Write data rows
    for item in items:
        writer.writerow([
            item.id,
            item.category.name,
            item.name,
            item.description,
            item.price,
            item.is_sold,
            item.stock,
            item.created_by.username,
            item.created_at
        ])

    return response