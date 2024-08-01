from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import Photo
from blog.views import get_categories

def gallery(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    context.update(get_categories())
    return render(request, 'gallery/index.html', context)

def media(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = PhotoForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'gallery/media.html', context)
