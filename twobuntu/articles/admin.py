from django.contrib import admin

from twobuntu.articles.models import Article, ScheduledArticle


class ArticleAdmin(admin.ModelAdmin):
    """
    Describe the administration inferface for articles.
    """

    def make_released(self, request, queryset):
        """
        Releases the articles under a CC BY-SA 4.0 license.
        """
        queryset.filter(author=request.user).update(cc_license=True)
    make_released.short_description = "Release articles under CC BY-SA 4.0 license"

    actions = (make_released,)
    date_hierarchy = 'date'
    list_display = ('title', 'author', 'date')
    list_filter = ('status', 'cc_license', 'category', 'author')
    search_fields = ('title', 'body')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ScheduledArticle)
