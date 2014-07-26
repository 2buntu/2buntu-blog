from django import forms

from twobuntu.news.models import Item


class AddItemForm(forms.ModelForm):
    """
    Form for adding news items.
    """

    class Meta:
        model = Item
        fields = ('title', 'body', 'url')
