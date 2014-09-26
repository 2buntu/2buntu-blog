from io import BytesIO
from math import ceil

from django.contrib.staticfiles import finders
from PIL import Image

# Coordinates for rendering the picture with and without the Unity panel
# Each item in the array represents a layer for the generator to render
# The format of the tuple is (filename, dest_x, dest_y, dest_w, dest_h)
TEMPLATES = [
    {
        'title': 'Meizu MX3 with Unity Panel',
        'dimensions': (1346, 2313),
        'layers': [
            (None, 131, 286, 1080, 1727),
            ('panel.png', 131, 213, 1080, 73),
            ('mx3.png', 0, 0, 1346, 2313),
        ],
    },
    {
        'title': 'Meizu MX3 without Unity Panel',
        'dimensions': (1346, 2313),
        'layers': [
            (None, 131, 213, 1080, 1800),
            ('mx3.png', 0, 0, 1346, 2313),
        ],
    },
]


def generate_device_art(template, image):
    """
    Combine the layers for the template into a final image.
    """
    # Create the final image upon which everything will be rendered
    t = TEMPLATES[template]
    o = Image.new('RGBA', t['dimensions'])
    # For each of the layers, resize and crop according to the definition, and blend
    for l in t['layers']:
        i = Image.open(finders.find('img/touch/%s' % l[0]) if l[0] else image)
        w, h = i.size
        i = i.crop((0, 0, w, int(ceil(float(l[4]) / float(l[3]) * w))))
        i = i.resize((l[3], l[4]), Image.ANTIALIAS)
        c = Image.new('RGBA', t['dimensions'])
        c.paste(i, (l[1], l[2]))
        o = Image.alpha_composite(o, c)
    # Return a file-like object representing the rendered picture
    response = BytesIO()
    o.save(response, format='PNG')
    return response.getvalue()
