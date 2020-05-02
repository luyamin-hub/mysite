from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.

class ReadNum(models.Model):
      read_num = models.IntegerField(default=0,verbose_name= "点击数")
      content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name= "点击模型")
      object_id = models.PositiveIntegerField(verbose_name= "模型id")
      content_object = GenericForeignKey('content_type', 'object_id')
      class Meta:
         verbose_name_plural = "点击计数"   

class ReadDetail(models.Model):
    read_num = models.IntegerField(default=0,verbose_name= "点击数")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name= "阅读模型")
    object_id = models.PositiveIntegerField(verbose_name= "模型id")
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateField(default=timezone.now,verbose_name= "阅读时间")
    class Meta:
      verbose_name_plural = "具体点击计数"   