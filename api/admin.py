from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    search_fields = ('name', )
    inlines = [ReviewInline, ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'text', 'score', 'author')
    inlines = [CommentInline, ]
