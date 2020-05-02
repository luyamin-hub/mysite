from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VideoType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):
        return self.type_name

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_cover_img = models.ImageField(upload_to='video/img',null=True)
    desc =models.CharField(max_length=200)
    video_type = models.ForeignKey(VideoType,on_delete=models.CASCADE)
    file_url = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=False)
    class Meta:
          ordering =['-create_time']            
    def __str__ (self):
        return "<Video: %s>" % self.title


