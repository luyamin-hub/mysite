from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name= "喜欢对象模型")
    object_id = models.PositiveIntegerField(verbose_name= "模型id")
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.IntegerField(default=0,verbose_name= "喜欢数量")
    class Meta:
      verbose_name_plural = "喜欢计数"    

class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name= "喜欢对象模型")
    object_id = models.PositiveIntegerField(verbose_name= "模型id")
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name= "喜欢用户")
    liked_time = models.DateTimeField(auto_now_add=True,verbose_name= "喜欢时间")
    class Meta:
      verbose_name_plural = "喜欢记录"   