from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from twobuntu.images.forms import ImageUploadForm

def upload(request):
    """Upload images for embedding in articles."""
    return render(request, 'images/upload.html', {
        'title': 'Upload',
        'form':  ImageUploadForm(),
        'description': "Use this form to upload an image.",
        'action': 'Upload',
    })
