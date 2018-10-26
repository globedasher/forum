from django.contrib import admin

# Register your models here.

from .models import Category, Post

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "private", "created_by", "created_at", "updated_at")


class PostAdmin(admin.ModelAdmin):
    list_display = ("owner", "category", "title", "body", "created_at", "updated_at")



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
