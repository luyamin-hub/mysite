from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserExtension(models.Model):
    SEX_CHOICES = (
        ('---','---'),
        ("男", "男"),
        ("女", "女"),
        ("保密", "保密")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension',verbose_name='用户名称')
    nickname = models.CharField(max_length=30, verbose_name='昵称',blank=True)
    sex = models.CharField(max_length=10,choices=SEX_CHOICES,verbose_name='性别',blank=True)
    telephone = models.CharField(max_length=11, verbose_name='电话号码')
    user_logo = models.ImageField(upload_to='user',verbose_name='头像',null=True)
    qq_number = models.CharField(max_length=20, verbose_name='QQ号',blank=True)
    birthday = models.DateField(null=True,verbose_name='出生日期',blank=True)
    school = models.CharField(max_length=20, verbose_name='学校',blank=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name='最后修改时间')

@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()

      