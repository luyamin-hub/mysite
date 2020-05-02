from django.shortcuts import render
from mysite.views import paginator_detail
from .models import PhotoAlbumType,PhotoAlbum
# Create your views here.
def photo(request):
    photo_all_list = PhotoAlbum.objects.all()
    context = {}
    context['photos'] = photo_all_list
    context['photo_types'] =PhotoAlbumType.objects.all()
    return render(request,'photo.html',context)
