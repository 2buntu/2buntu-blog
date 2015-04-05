from io import BytesIO
from os import path

from PIL import Image


# Each entry in the list contains the information necessary to render the final
# image with each of the layers resized and cropped accordingly. Some of this
# information is also required by the JavaScript on the page.
TEMPLATES = {
    'bq-aquaris': {
        'title': 'BQ Aquaris E4.5 Ubuntu Edition',
        'frame': (671, 1305),
        'screen': (540, 960),
        'offset': (65, 145),
    },
    'meizu-mx3': {
        'title': 'Meizu MX3',
        'frame': (1346, 2313),
        'screen': (1080, 1800),
        'offset': (131, 213),
    },
}


def blit_source_image(output, template, image):
    """
    Blit the source image to the output image, scaling and cropping as needed.
    """
    img = Image.open(image)
    screen = TEMPLATES[template]['screen']
    factor = float(screen[0]) / float(img.size[0])
    dimensions = [int(i * factor) for i in img.size]
    img = img.resize(dimensions, Image.ANTIALIAS)
    img = img.crop([0, 0] + [min(*i) for i in zip(dimensions, screen)])
    output.paste(img, TEMPLATES[template]['offset'])


def blit_template_image(output, template, filename):
    """
    Blit the specified file from the template to the output image.
    """
    img = Image.open(path.join(path.dirname(__file__), 'img', template, filename))
    return Image.alpha_composite(output, img)


def generate_device_art(template, image, panel, glossy):
    """
    Combine the layers for the template into a final image.
    """
    output = Image.new('RGBA', TEMPLATES[template]['frame'])
    blit_source_image(output, template, image)
    output = blit_template_image(output, template, 'frame.png')
    if glossy:
        output = blit_template_image(output, template, 'gloss.png')
    response = BytesIO()
    output.save(response, format='PNG')
    return response.getvalue()
