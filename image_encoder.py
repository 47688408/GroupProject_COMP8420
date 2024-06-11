import base64


def encode_image(image):
    return base64.b64encode(image.getvalue()).decode('utf-8')
