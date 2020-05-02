from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.conf import settings
from django.db.models import Count
from mysite.views import paginator_detail
from read_statistics.utils import read_statistics_once_read
# Create your views here.
# 获取博客分类的对应博客数量
def blog_class_data(request):
    blog_dates = Blog.objects.dates('create_time','month',order="DESC")
    blog_dates_dict ={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                          create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {}
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    page_of_blogs,page_range = paginator_detail(request,blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    context = {}
    context = blog_class_data(request)
    context['blogs'] = blogs_all_list 
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    return render(request,'blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    page_of_blogs,page_range = paginator_detail(request,blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    context = {}  
    context = blog_class_data(request)
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_type'] = blog_type
    return render(request,'blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    page_of_blogs,page_range = paginator_detail(request,blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    context = {}  
    context = blog_class_data(request)
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render(request,'blogs_with_date.html',context)

def blog_detail(request,blog_pk):  
    blog = get_object_or_404(Blog,pk=blog_pk) 
    read_cookie_key = read_statistics_once_read(request,blog)   
    context = {}  
    context = blog_class_data(request)
    context['blog'] = blog
    context ['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context ['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    response=render(request,'blog_detail.html',context)
    response.set_cookie(read_cookie_key ,'true')
    return response