# from django.contrib import admin
# from .models import Tweet
# # Register your models here.

# admin.site.register(Tweet)
# class TweetAdmin(admin.ModelAdmin):
#     list_display = ('user', 'text', 'created_at')
from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')

