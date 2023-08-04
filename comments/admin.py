from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_date', 'modified_date')
    search_fields = ('user__username', 'product__name', 'text')

admin.site.register(Comment, CommentAdmin)
