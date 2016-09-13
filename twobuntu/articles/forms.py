from django import forms

from twobuntu.articles.models import Article, ScheduledArticle


class EditorForm(forms.ModelForm):
    """
    Form for entering or editing articles.
    """

    # The <textarea> needs this set so that the form can validate on the client
    # side without any content (due to ACE editor)
    use_required_attribute = False

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


class DeleteArticleForm(forms.Form):
    """
    Form for deleting articles.
    """

    # Intentionally blank - submitting the form
    # is considered consent to delete the article.
