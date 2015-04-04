from io import BytesIO

from django.contrib.staticfiles import finders
from PIL import Image


# Each entry in the list contains the information necessary to render the final
# image with each of the layers resized and cropped accordingly. This
# information is also required by the JavaScript on the page.
TEMPLATES = [
    {
        'name': 'bq-aquaris',
        'title': 'BQ Aquaris E4.5 Ubuntu Edition',
        'image_dimensions': (671, 1305),
        'screen_dimensions': (540, 960),
        'screen_offset': (65, 145),
    },
    {
        'name': 'meizu-mx3',
        'title': 'Meizu MX3',
        'image_dimensions': (1346, 2313),
        'screen_dimensions': (1080, 1800),
        'screen_offset': (131, 213),
    }
]


def generate_device_art(template, image, glossy):
    """
    Combine the layers for the template into a final image.
    """
    # Create the final image upon which everything will be rendered
    t = TEMPLATES[template]
    o = Image.new('RGBA', t['image_dimensions'])
    # Open the image uploaded by the user
    i = Image.open(image)
    w, h = i.size
    # Scale the image to match the width of the screen
    sd = t['screen_dimensions']
    a = float(sd[0]) / float(w)
    w, h = int(w * a), int(h * a)
    i = i.resize((w, h), Image.ANTIALIAS)
    i = i.crop((0, 0, min(w, sd[0]), min(h, sd[1])))
    # Blit the uploaded image to the output image
    o.paste(i, t['screen_offset'])
    # Blit the frame
    i = Image.open(finders.find('img/touch/%s/frame.png' % t['name']))
    o = Image.alpha_composite(o, i)
    # Optionally blit the glossy overlay
    if glossy:
        i = Image.open(finders.find('img/touch/%s/gloss.png' % t['name']))
        print i.size, o.size
        o = Image.alpha_composite(o, i)
    # Return a file-like object representing the rendered picture
    response = BytesIO()
    o.save(response, format='PNG')
    return response.getvalue()
