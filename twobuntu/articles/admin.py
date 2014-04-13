from django.contrib import admin

from twobuntu.articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    """Describe the administration inferface for articles."""

    date_hierarchy = 'date'
    list_display   = ('title', 'author', 'date',)
    list_filter    = ('status', 'cc_license', 'category', 'author',)
    search_fields  = ('title', 'body',)

admin.site.register(Article, ArticleAdmin)
