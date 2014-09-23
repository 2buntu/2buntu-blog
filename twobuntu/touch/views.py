from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from PIL import Image

from twobuntu.touch.forms import DeviceArtForm


def generate_device_art(screenshot):
    """
    Load the template and combine it with the screenshot.
    """
    response = BytesIO()
    t = Image.open(finders.find('img/touch-frame.png'))
    s = Image.open(screenshot)
    s.thumbnail((319, 543), Image.ANTIALIAS)
    t.paste(s, (41, 109))
    t.save(response, format='PNG')
    return response.getvalue()


def generator(request):
    """
    Generate a picture of a device with a screenshot.
    """
    if request.method == 'POST':
        form = DeviceArtForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            response = HttpResponse(generate_device_art(request.FILES['image']), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="ubuntu-touch-device-art.png"'
            return response
    else:
        form = DeviceArtForm()
    return render(request, 'touch/generator.html', {
        'title': 'Device Art Generator',
        'form': form,
    })
