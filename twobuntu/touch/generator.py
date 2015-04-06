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
        'panel': 37,
    },
    'meizu-mx3': {
        'title': 'Meizu MX3',
        'frame': (1346, 2313),
        'screen': (1080, 1800),
        'offset': (131, 213),
        'panel': 73,
    },
}


def blit_source_image(output, template, image, panel):
    """
    Blit the source image to the output image, scaling and cropping as needed.
    """
    img = Image.open(image)
    screen = TEMPLATES[template]['screen']
    factor = float(screen[0]) / float(img.size[0])
    dimensions = [int(i * factor) for i in img.size]
    if panel:
        dimensions[1] -= TEMPLATES[template]['panel']
    img = img.resize(dimensions, Image.ANTIALIAS)
    img = img.crop([0, 0] + [min(*i) for i in zip(dimensions, screen)])
    offset = list(TEMPLATES[template]['offset'])
    if panel:
        offset[1] += TEMPLATES[template]['panel']
    output.paste(img, tuple(offset))


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
    blit_source_image(output, template, image, panel)
    if panel:
        output = blit_template_image(output, template, 'panel.png')
    output = blit_template_image(output, template, 'frame.png')
    if glossy:
        output = blit_template_image(output, template, 'gloss.png')
    response = BytesIO()
    output.save(response, format='PNG')
    return response.getvalue()
