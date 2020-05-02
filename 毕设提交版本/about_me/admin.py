from django.contrib import admin
from .models import AboutMe 
# Register your models here.
@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('id','title','introduction')