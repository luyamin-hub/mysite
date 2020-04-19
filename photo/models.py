from django.db import models
from django.utils import timezone
# Create your models here.
class PhotoAlbumType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__ (self):
        return self.type_name

class PhotoAlbum(models.Model):
    photo_img = models.ImageField(upload_to='photo',null=True)
    title = models.CharField(max_length=50)
    photo_type = models.ForeignKey(PhotoAlbumType,on_delete=models.CASCADE)
    brief_introduction= models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    class Meta:
          ordering =['-create_time']            
    def __str__ (self):
        return "<PhotoAlbum: %s>" % self.title