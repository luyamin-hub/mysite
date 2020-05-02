from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VideoType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name= "视频类型")
    class Meta:
      verbose_name_plural = "视频类型"  

    def __str__ (self):
        return self.type_name

class Video(models.Model):
    title = models.CharField(max_length=100,verbose_name= "标题")
    video_cover_img = models.ImageField(upload_to='video/img',null=True,verbose_name= "视频cover照片")
    desc =models.CharField(max_length=200,verbose_name= "简单介绍")
    video_type = models.ForeignKey(VideoType,on_delete=models.CASCADE,verbose_name= "类型")
    file_url = models.CharField(max_length=255,verbose_name= "视频路由")
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name= "作者")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name= "创建时间")
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name= "最后修改时间")
    is_publish = models.BooleanField(default=False,verbose_name= "是否发布")
    class Meta:
          ordering =['-create_time'] 
          verbose_name_plural = "视频"             
    def __str__ (self):
        return "<Video: %s>" % self.title


