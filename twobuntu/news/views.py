import twitter
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import redirect, render

from twobuntu.news.forms import AddItemForm


@user_passes_test(lambda u: u.is_staff)
def add(request):
    """
    Add news items to the home page.
    """
    if request.method == 'POST':
        form = AddItemForm(data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.reporter = request.user
            try:
                with transaction.atomic():
                    item.save()
            except twitter.TwitterError as e:
                messages.error(request, "Twitter error: \"%s\" Please try again." % e.message[0]['message'])
            else:
                messages.info(request, "Your news item has been published!")
                return redirect('home')
    else:
        form = AddItemForm()
    return render(request, 'form.html', {
        'title': 'Add Item',
        'form': form,
        'description': "Enter the details for the news item below.",
        'action': 'Add',
    })
