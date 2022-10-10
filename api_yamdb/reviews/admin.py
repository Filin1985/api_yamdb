from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'rating', 'description', 'category',  # 'genre',
    )
    list_editable = ('name', 'year', 'description', 'category',)  # 'genre'
    search_fields = ('name', 'description')
    list_filter = ('year', 'rating', 'category')  # 'genre',
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    list_editable = ('title', 'text', 'author', 'score',)
    search_fields = ('text', 'title')
    list_filter = ('pub_date', 'author', 'title', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
