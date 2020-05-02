from django.shortcuts import render,get_object_or_404
from .models import AboutMe
from blog.models import Blog
# Create your views here.
def about_me(request):
    # recommend_blogs = Blog.objects.filter(recommend_blog=True)[:5] 
    about_me = AboutMe.objects.all().first()
    recommend_blogs = Blog.objects.filter(recommend_blog=True)[:5] 
    new_blogs = Blog.objects.all()[:8]
    context = {}
    context['about_me'] = about_me
    context['recommend_blogs'] = recommend_blogs
    context['new_blogs'] = new_blogs
    return render(request,'about_me.html',context)