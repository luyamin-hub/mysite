from django.shortcuts import render,get_object_or_404
from video.models import Video,VideoType
from read_statistics.utils import read_statistics_once_read
# Create your views here.

def video(request):
    videos_all_list = Video.objects.all()
    context = {}
    context['videos'] =videos_all_list
    context['video_types'] =VideoType.objects.all()
    response=render(request,'video.html',context)
    video_pk = request.COOKIES.get('video_pk')
    if video_pk:
                 video=get_object_or_404( Video,pk=video_pk)
                 read_cookie_key = read_statistics_once_read(request,video) 
                 response=render(request,'video.html',context)
                 response.set_cookie(read_cookie_key ,'true')
    return response


 
