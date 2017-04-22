from django.contrib import admin
from .models import Post, Category, Tag


# 显示文章后台
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 显示分类后台
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


# 显示标签后台
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
