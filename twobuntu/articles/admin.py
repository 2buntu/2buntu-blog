from django.contrib import admin

from twobuntu.articles.models import Article

def make_released(modeladmin, request, queryset):
    """Releases the articles under a CC BY-SA 4.0 license."""
    queryset.update(cc_license=True)
make_released.short_description = "Release articles under CC BY-SA 4.0 license"

class ArticleAdmin(admin.ModelAdmin):
    """Describe the administration inferface for articles."""

    actions = (make_released,)
    date_hierarchy = 'date'
    list_display = ('title', 'author', 'date',)
    list_filter = ('status', 'cc_license', 'category', 'author',)
    search_fields = ('title', 'body',)

admin.site.register(Article, ArticleAdmin)
