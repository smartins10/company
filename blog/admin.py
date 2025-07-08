from django.contrib import admin
from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    list_filter = ('author', 'tag', 'date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post')
    list_filter = ('post',)
    search_field = ('user_name',)



# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
