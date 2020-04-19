from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):
        return self.type_name

class Blog(models.Model):
    blog_logo_img = models.ImageField(upload_to='blog/blog_img',null=True)
    brief_introduction=RichTextUploadingField()
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    recommend_blog = models.BooleanField(default=False)
    class Meta:
          ordering =['-create_time']            
    def __str__ (self):
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def get_title(self):
        return self.title

    