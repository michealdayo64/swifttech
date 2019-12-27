from django.contrib import admin
from .models import Post, Comment, Authur, Newletter
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'publish', 'status')
    list_filter = ('created','author',  'publish', 'status')
    search_fields = ('title', 'descriptions')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_field = ('authur')
    date_heirarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)
#admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Authur)
admin.site.register(Newletter)