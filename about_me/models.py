from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class AboutMe(models.Model):
    title = models.CharField(max_length=50)
    introduction=RichTextUploadingField()
    
    def __str__ (self):
        return "<AboutMe: %s>" % self.title
    def get_title(self):
        return self.introduction