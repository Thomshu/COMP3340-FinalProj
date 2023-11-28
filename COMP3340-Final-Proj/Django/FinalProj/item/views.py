from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm, ImageForm
from .models import Category, Item, Images

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect


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
            return JsonResponse({'html_content': html_content, 'numPages': numPages}, content_type='application/json')

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
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

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
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index') #after deleting return to dashboard