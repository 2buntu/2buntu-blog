from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from PIL import Image

from twobuntu.touch.forms import DeviceArtForm

# Dimensions for the area of the frame used for the screenshot
SCREENSHOT_X = 41
SCREENSHOT_Y = 109
SCREENSHOT_W = 319
SCREENSHOT_H = 543


def generate_device_art(screenshot):
    """
    Load the template and combine it with the screenshot.
    """
    response = BytesIO()
    t = Image.open(finders.find('img/touch-frame.png'))
    s = Image.open(screenshot)
    w, h = s.size
    s = s.crop((0, 0, w, int(float(SCREENSHOT_H) / float(SCREENSHOT_W) * w)))
    s = s.resize((SCREENSHOT_W, SCREENSHOT_H), Image.ANTIALIAS)
    t.paste(s, (SCREENSHOT_X, SCREENSHOT_Y))
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
