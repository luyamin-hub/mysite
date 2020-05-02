from django.contrib import admin
from .models import UserExtension    
# Register your models here.
@admin.register(UserExtension)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','user','nickname','sex','telephone' ,'qq_number','create_time','last_updated_time')