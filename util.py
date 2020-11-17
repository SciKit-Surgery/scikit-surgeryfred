"""Utilities
"""
import re
import base64

import numpy as np

from PIL import Image, ImageDraw
from io import BytesIO
from itertools import chain


def base64_to_pil(img_base64):
    """
    Convert base64 image data to PIL image
    """
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image


def np_to_base64(img_np):
    """
    Convert numpy image (RGB) to base64 string
    """
    img = Image.fromarray(img_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")


def contour_to_image(template_image, contour):
    """
    Creates a contour image
    
    :params template_image: used to set the dimensions of the output image
    :params contour: set of 2D points defining the contour
    :returns: a PIL image.
    """
    out_image = Image.new('RGB', (template_image.size), color = 'white')
    draw = ImageDraw.Draw(out_image)

    xy_swap = [(swap[1], swap[0]) for swap in contour.astype(int)]
    draw.line((list(chain(*xy_swap))), fill = (255,0,0))
    return out_image
