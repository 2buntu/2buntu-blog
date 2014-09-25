from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from PIL import Image

from twobuntu.touch.forms import DeviceArtForm

# Dimensions used for calculations
TEMPLATE_W = 1346
TEMPLATE_H = 2313
SCREENSHOT_X = 131
SCREENSHOT_Y = 213
SCREENSHOT_W = 1080
SCREENSHOT_H = 1800


def generate_device_art(screenshot):
    """
    Load the template & overlay and combine them with the screenshot.
    """
    response = BytesIO()
    # Open the two images to be combined
    s = Image.open(screenshot)
    t = Image.open(finders.find('img/touch-frame.png'))
    # Crop and resize the screenshot
    w, h = s.size
    s = s.crop((0, 0, w, int(float(SCREENSHOT_H) / float(SCREENSHOT_W) * w)))
    s = s.resize((SCREENSHOT_W, SCREENSHOT_H), Image.ANTIALIAS)
    # Create the output image and paste the screenshot on it
    o = Image.new('RGBA', (TEMPLATE_W, TEMPLATE_H))
    o.paste(s, (SCREENSHOT_X, SCREENSHOT_Y))
    # Blend the frame above and save the image to the BytesIO
    Image.alpha_composite(o, t).save(response, format='PNG')
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
