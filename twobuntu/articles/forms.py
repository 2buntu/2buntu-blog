from django import forms

from twobuntu.articles.models import Article, ScheduledArticle


class EditorForm(forms.ModelForm):
    """
    Form for entering or editing articles.
    """

    class Meta:
        model = Article
        fields = ('category', 'title', 'body')


class ScheduledArticleForm(forms.ModelForm):
    """
    Form for scheduling articles.
    """

    class Meta:
        model = ScheduledArticle
        fields = ('date',)
