from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from twobuntu.images.forms import ImageUploadForm
from twobuntu.images.models import Image


@login_required
def view(request, id):
    """
    View uploaded image.
    """
    image = get_object_or_404(Image, pk=id)
    return render(request, 'images/view.html', {
        'title': image.caption,
        'image': image,
    })


@login_required
def upload(request):
    """
    Upload images for embedding in articles.
    """
    js = 'js' in request.GET
    if request.method == 'POST':
        form = ImageUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save()
            if js:
                return HttpResponse('<script>window.opener.editor.insertImage("[image:%d]");window.close();</script>' % image.id)
            else:
                return redirect(image)
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload.html', {
        'title': 'Upload',
        'form': form,
        'description': "Use this form to upload an image.",
        'action': 'Upload',
        'js': js,
    })
