from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from twobuntu.images.forms import ImageUploadForm

@login_required
def upload(request):
    """Upload images for embedding in articles."""
    if request.method == 'POST':
        form = ImageUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save()
            messages.info(request, "Your image has been uploaded and can be embedded with \"[image:%d]\"." % image.id)
            return redirect('home')
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload.html', {
        'title': 'Upload',
        'form':  form,
        'description': "Use this form to upload an image.",
        'action': 'Upload',
    })
