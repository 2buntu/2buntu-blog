from django.http import HttpResponse
from django.shortcuts import render

from twobuntu.touch.forms import DeviceArtForm
from twobuntu.touch.generator import generate_device_art


def generator(request):
    """
    Generate a picture of a device with a user-supplied image.
    """
    if request.method == 'POST':
        form = DeviceArtForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = generate_device_art(
                form.cleaned_data['template'],
                request.FILES['image'],
                form.cleaned_data['add_panel'],
                form.cleaned_data['glossy_screen'],
            )
            response = HttpResponse(image, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="ubuntu-touch-device-art.png"'
            response['Content-Length'] = len(image)
            return response
    else:
        form = DeviceArtForm()
    return render(request, 'touch/generator.html', {
        'title': 'Device Art Generator',
        'form': form,
    })
