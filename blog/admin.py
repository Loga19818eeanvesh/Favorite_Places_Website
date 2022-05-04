from csv import list_dialects
from django.contrib import admin

from .models import Tag,Post,Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("title",)}
    list_filter = ("date","address","tags")
    list_display = ("title","address","date","author")

class TagAdmin(admin.ModelAdmin):
    list_display = ("caption",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post")
    list_filter = ("post","user")


admin.site.register(Post,PostAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)
