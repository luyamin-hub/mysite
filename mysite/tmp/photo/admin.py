from django.contrib import admin
from .models import PhotoAlbumType,PhotoAlbum   
# Register your models here.
@admin.register(PhotoAlbumType)
class PhotoAlbumType(admin.ModelAdmin):
    list_display = ('id','type_name')
@admin.register(PhotoAlbum)
class PhotoAlbum(admin.ModelAdmin):
    list_display = ('id','title','photo_type','brief_introduction','create_time','last_updated_time') 