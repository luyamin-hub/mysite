from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class AboutMe(models.Model):
    title = models.CharField(max_length=50,verbose_name= "评论标题")
    introduction=RichTextUploadingField(verbose_name= "评论介绍")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = "创建时间")
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name = "最后修改时间")
    class Meta:
      ordering =['-create_time']  
      verbose_name_plural = "关于我"     
    def __str__ (self):
        return "<AboutMe: %s>" % self.title
    def get_title(self):
        return self.introduction