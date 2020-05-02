from django.contrib import admin
from .models import VideoType,Video  
# Register your models here.
@admin.register(VideoType)
class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','title','video_type','is_publish','create_time','last_updated_time') 