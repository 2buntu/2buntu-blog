from django import forms

from twobuntu.articles.models import Article

class EditorForm(forms.ModelForm):
    """Form for entering or editing articles."""

    class Meta:
        model = Article
        fields = ('category', 'title', 'body',)
