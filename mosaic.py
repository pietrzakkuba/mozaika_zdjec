from requests import get
from PIL import Image
from random import shuffle
from os import remove
from glob import glob


def add_frame(image):  # adding frames to images so they look better as a mosaic
    new_size = (int(image.size[0] * 1.05), int(image.size[1] * 1.05))
    new_image = Image.new('RGB', new_size, (0, 0, 0))
    new_image.paste(image, (int(0.025 * image.size[0]), int(0.025 * image.size[1])))
    return new_image


def download_image(address, nr):
    name = '0' + str(nr) + '.jpg'
    file = open(name, 'wb')
    file.write(get(address).content)
    file.close()
    image = Image.open(name)
    image = add_frame(image)
    image.save(name)


def remove_files():
    for name in glob('0*.jpg'):
        remove(name)


def error(max_width, max_height):
    background = Image.new('RGB', (max_width, max_height), (255, 0, 0))  # red background if wrong number of images given
    background.save('result.jpg')


def fit_in_background(image, max_width, max_height):  # paste final picture in the centre of the background
    image = add_frame(image)
    background = Image.new('RGB', (max_width, max_height), (0, 0, 0))  # background has a size given in url
    width1, height1 = image.size
    ratio = min(max_width / width1, max_height / height1)  # adjusting image size
    new_width1 = int(ratio * width1)
    new_height1 = int(ratio * height1)
    image = image.resize((new_width1, new_height1))
    if new_width1 in (max_width - 1, max_width, max_width + 1):  # +/- 1 pixel tolerance for rounding from float to int
        point = (0, int(max_height / 2 - new_height1 / 2))  # finding right place to paste
    else:
        point = (int(max_width / 2 - new_width1 / 2), 0)
    background.paste(image, point)
    background.save('result.jpg')  # save result


def two_horizontally(image1, image2):  # taking two pictures and combine them horizontally
    width1, height1 = image1.size
    width2, height2 = image2.size
    width2 = int(width2 * (height1 / height2))
    height2 = height1
    image2 = image2.resize((width2, height2))
    combined = Image.new('RGB', ((width1 + width2), height1))
    combined.paste(image1, (0, 0))
    combined.paste(image2, (width1, 0))
    return combined


def three_horizontally(image1, image2, image3):
    image = two_horizontally(image1, image2)
    return two_horizontally(image, image3)


def two_vertically(image1, image2):  # taking two pictures and combine them vertically
    width1, height1 = image1.size
    width2, height2 = image2.size
    height2 = int(height2 * (width1 / width2))
    width2 = width1
    image2 = image2.resize((width2, height2))
    combined = Image.new('RGB', (width1, (height1 + height2)))
    combined.paste(image1, (0, 0))
    combined.paste(image2, (0, height1))
    return combined


def three_vertically(image1, image2, image3):
    image = two_vertically(image1, image2)
    return two_vertically(image, image3)


def one(max_width, max_height):
    image1 = Image.open('00.jpg')  # just one image
    fit_in_background(image1, max_width, max_height)


def two(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_vertically(image1, image2)  # two pictures combined vertically
    fit_in_background(image12, max_width, max_height)


def three(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_horizontally(image1, image2)  # 2 pictures combined horizontally on the top
    image3 = Image.open('02.jpg')
    image123 = two_vertically(image12, image3)  # 3rd picture added to the bottom
    fit_in_background(image123, max_width, max_height)


def four(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_horizontally(image1, image2)  # 2 pictures combined horizontally on the top
    image3 = Image.open('02.jpg')
    image4 = Image.open('03.jpg')
    image34 = two_horizontally(image3, image4)  # other 2 pictures combined horizontally on the bottom
    image1234 = two_vertically(image12, image34)  # two created sets combined together vertically making 2x2
    fit_in_background(image1234, max_width, max_height)


def five(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_horizontally(image1, image2)  # top horizontal layer
    image3 = Image.open('02.jpg')
    image4 = Image.open('03.jpg')
    image5 = Image.open('04.jpg')
    image45 = two_horizontally(image4, image5)  # bottom horizontal layer
    image12345 = three_vertically(image12, image3, image45)  # combining bottom with top and middle
    fit_in_background(image12345, max_width, max_height)


def six(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_horizontally(image1, image2)  # top horizontal layer
    image3 = Image.open('02.jpg')
    image4 = Image.open('03.jpg')
    image34 = two_horizontally(image3, image4)  # middle horizontal layer
    image5 = Image.open('04.jpg')
    image6 = Image.open('05.jpg')
    image56 = two_horizontally(image5, image6)  # bottom horizontal layer
    image123456 = three_vertically(image12, image34, image56)  # combining layers
    fit_in_background(image123456, max_width, max_height)


def seven(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image12 = two_horizontally(image1, image2)  # top horizontal layer
    image3 = Image.open('02.jpg')
    image4 = Image.open('03.jpg')
    image5 = Image.open('04.jpg')
    image345 = three_horizontally(image3, image4, image5)  # middle horizontal layer
    image6 = Image.open('05.jpg')
    image7 = Image.open('06.jpg')
    image67 = two_horizontally(image6, image7)  # bottom horizontal layer
    image1234567 = three_vertically(image12, image345, image67)  # combining layers
    fit_in_background(image1234567, max_width, max_height)


def eight(max_width, max_height):
    image1 = Image.open('00.jpg')
    image2 = Image.open('01.jpg')
    image3 = Image.open('02.jpg')
    image123 = three_horizontally(image1, image2, image3)  # top horizontal layer
    image4 = Image.open('03.jpg')
    image5 = Image.open('04.jpg')
    image45 = two_horizontally(image4, image5)  # middle horizontal layer
    image6 = Image.open('05.jpg')
    image7 = Image.open('06.jpg')
    image8 = Image.open('07.jpg')
    image678 = three_horizontally(image6, image7, image8)  # bottom horizontal layer
    image12345678 = three_vertically(image123, image45, image678)  # combining layers
    fit_in_background(image12345678, max_width, max_height)


def produce_image(random, res, urls):
    number_of_photos = urls[0]  # getting number of photos
    if random:
        shuffle(urls[1])  # shuffling order if random == True
    for i in range(number_of_photos):
        download_image(urls[1][i], i)  # downloading images
    if number_of_photos == 1:  # "switch-case"
        one(int(res[0]), int(res[1]))
    elif number_of_photos == 2:
        two(int(res[0]), int(res[1]))
    elif number_of_photos == 3:
        three(int(res[0]), int(res[1]))
    elif number_of_photos == 4:
        four(int(res[0]), int(res[1]))
    elif number_of_photos == 5:
        five(int(res[0]), int(res[1]))
    elif number_of_photos == 6:
        six(int(res[0]), int(res[1]))
    elif number_of_photos == 7:
        seven(int(res[0]), int(res[1]))
    elif number_of_photos == 8:
        eight(int(res[0]), int(res[1]))
    else:
        error(int(res[0]), int(res[1]))  # showing red background with no mosaic
    remove_files()

