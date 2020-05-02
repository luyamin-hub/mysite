# Generated by Django 2.0 on 2020-04-24 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-create_time'], 'verbose_name_plural': '视频'},
        ),
        migrations.AlterModelOptions(
            name='videotype',
            options={'verbose_name_plural': '视频类型'},
        ),
        migrations.AlterField(
            model_name='video',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='video',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='简单介绍'),
        ),
        migrations.AlterField(
            model_name='video',
            name='file_url',
            field=models.CharField(max_length=255, verbose_name='视频路由'),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='是否发布'),
        ),
        migrations.AlterField(
            model_name='video',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='最后修改时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_cover_img',
            field=models.ImageField(null=True, upload_to='video/img', verbose_name='视频cover照片'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.VideoType', verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='videotype',
            name='type_name',
            field=models.CharField(max_length=15, verbose_name='视频类型'),
        ),
    ]
