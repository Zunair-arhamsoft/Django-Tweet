from django.contrib import admin

from .models import Tweet   
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'updated_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)
    ordering = ('-created_at',)