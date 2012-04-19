from similus import compare, get_data, compare_data
import ImageFont
import ImageDraw
import ImageChops
import Image
from path import path

def autocrop(im, bgcolor):
    if im.mode != "RGB":
        im = im.convert("RGB")
    bg = Image.new("RGB", im.size, bgcolor)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return None # no contents

class Crab(object):
    def __init__(self):
        self.images = []

    def load(images):
        for image in images:
            self.images.append((get_data(image), image))

    def __len__(self):
        return len(self.images)

    def compare_many(self, image, sort=True):
        '''
        if sort is falsy, a generator is returned and results come in the order
        images were loaded, else a sorted list is returned
        '''
        if not self.images:
            raise IndexError('No images loaded')
        image_data = get_data(image)
        comparisons = ((other_image, compare_data(image_data, other_image_data)) for
                       other_image_data, other_image in self.images)
        if sort:
            return sorted(comparisons, key=lambda x:x[1])
        return comparisons

    def clear(self):
        self.images = []
            
class Otter(object):
    def __init__(self, directory=None):
        if directory:
            self.load_images(path(directory).files())

    def create_images(self, font, alphabet, directory, font_size=14):
        font = ImageFont.truetype(font, font_size)
        directory = path(directory)
        directory.makedirs_p()
        for char in alphabet:
            self.create_char(font, char, directory, font_size)

    def create_char(self, font, char, directory, font_size):
        im_size = (font_size*2, font_size*2)
        img = Image.new("RGB", im_size, (255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((2, 2), char, (0,0,0), font=font)
        img = autocrop(img, 'white')
#        img.show()
        img_path = path(directory).joinpath('%05d.png' % ord(char))
        img.save(img_path)
        print img_path

    def load_images(self, image_files):
        for f in image_files:
            pass
            
if __name__ == '__main__':
    import string
    alphabet = string.letters + string.digits
    otter = Otter()
    otter.create_images('/home/ddd/Dropbox/prog/sc2wow/bl.ttf', alphabet=alphabet, directory='similus_images')
