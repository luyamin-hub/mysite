from django.db import models
from django.utils import timezone
# Create your models here.
class PhotoAlbumType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name= "照片类型")
    class Meta:
      verbose_name_plural = "照片类型"   
    def __str__ (self):
        return self.type_name

class PhotoAlbum(models.Model):
    photo_img = models.ImageField(upload_to='photo',null=True,verbose_name= "相册照片")
    title = models.CharField(max_length=50,verbose_name= "标题")
    photo_type = models.ForeignKey(PhotoAlbumType,on_delete=models.CASCADE,verbose_name= "类型")
    brief_introduction= models.CharField(max_length=100,verbose_name= "简单介绍")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name= "创建时间")
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name= "最后修改时间")
    class Meta:
          ordering =['-create_time'] 
          verbose_name_plural = "相册"             
    def __str__ (self):
        return "<PhotoAlbum: %s>" % self.title