from flask import Flask, send_file, request
from mosaic import produce_image

app = Flask(__name__)


@app.route('/')
def index():
    return '<a href=mozaika>Go to /mozaika and type parameters</a>'  # index


def manage_randomness(text):
    if text == '1':
        return True
    return False


def manage_resolution(text):
    width = text.split('x')[0]
    height = text.split('x')[1]
    return width, height


def manage_photos(text):
    urls = text.split(',')
    length = len(urls)
    return length, urls


@app.route('/mozaika')
def get_image():
    test_random_order = request.args.get('losowo')
    if test_random_order is not None:
        random_order = manage_randomness(test_random_order)
    else:
        random_order = False
    test_resolution = request.args.get('rozdzielczosc')
    if test_resolution is not None:
        resolution = manage_resolution(test_resolution)
    else:
        resolution = ('2048', '2048')
    test_photos = request.args.get('zdjecia')
    if test_photos is not None:
        photos = manage_photos(test_photos)
    else:
        photos = (0, [])
    produce_image(random_order, resolution, photos)
    return send_file('result.jpg')


if __name__ == '__main__':
    app.run()
