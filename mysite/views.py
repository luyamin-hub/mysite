from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from blog.models import Blog
from video.models import Video
from read_statistics.utils import get_seven_days_read_data
#分页器
def paginator_detail(request,paginator_obj,paginator_each_num):
    paginator =Paginator(paginator_obj,paginator_each_num)
    page_num =request.GET.get('page',1)
    page_of_objs =paginator.get_page(page_num)
    current_page_num=page_of_objs.number
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    if page_range[0] -1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return page_of_objs,page_range

def search(request):
    search_words = request.GET.get('wd', '').strip()
    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    
    search_blogs = []
    if condition is not None:
        # 筛选：搜索
        search_blogs = Blog.objects.filter(condition)

    # 分页
    page_of_blogs,page_range = paginator_detail(request,search_blogs,settings.EACH_PAGE_SEARCHS_NUMBER)
    context = {}
    context['search_words'] = search_words
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    return render(request, 'search.html', context)

def home(request):
    recommend_blogs = Blog.objects.filter(recommend_blog=True)[:5] 
    new_blogs = Blog.objects.all()[:8]
    context = {}
    page_of_blogs,page_range = paginator_detail(request,new_blogs,settings.EACH_PAGE_BLOGS_NUMBER)
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['recommend_blogs'] = recommend_blogs
    context['new_blogs'] = new_blogs
    #最近七天的博客阅读量及时间对应
    blog_content_type =ContentType.objects.get_for_model(Blog)
    # blog_read_nums = cache.get('blog_read_nums')
    # blog_dates = cache.get('blog_dates')
    # #设置数据库缓存信息
    # if blog_read_nums and blog_dates is None:
    blog_dates,blog_read_nums =get_seven_days_read_data(blog_content_type)
       # cache.set('blog_read_nums',blog_read_nums,3600)
       # cache.set('blog_dates',blog_dates,3600)

    context['blog_read_nums'] =blog_read_nums
    context['blog_dates'] = blog_dates
    
    #最近七天的视频阅读量及时间对应
    video_content_type =ContentType.objects.get_for_model(Video)
    # video_read_nums = cache.get('video_read_nums')
    # video_dates = cache.get('video_dates')
    # #设置数据库缓存信息
    # if video_read_nums and video_dates is None:
    video_dates,video_read_nums =get_seven_days_read_data(video_content_type)
       # cache.set('video_read_nums',blog_read_nums,3600)
       # cache.set('video_dates',blog_dates,3600)
    #最近七天的视频阅读量及时间对应
    context['video_read_nums'] =video_read_nums
    context['video_dates'] = video_dates

    return render(request,'home.html',context)


