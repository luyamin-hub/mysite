from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name= "博客分类")
    class Meta:
          verbose_name_plural = "博客分类"   

    def __str__ (self):
        return self.type_name

class Blog(models.Model):
    blog_logo_img = models.ImageField(upload_to='blog/blog_img',null=True,verbose_name= "博客照片")
    brief_introduction=RichTextUploadingField(verbose_name= "简单介绍")
    title = models.CharField(max_length=50,verbose_name = "标题")
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE,verbose_name = "类型")
    content = RichTextUploadingField(verbose_name = "内容")
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = "作者")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = "创建时间")
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name = "最后修改时间")
    recommend_blog = models.BooleanField(default=False,verbose_name = "是否推荐")
    class Meta:
          ordering =['-create_time']  
          verbose_name_plural = "博客"     
    def __str__ (self):
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def get_title(self):
        return self.title

    