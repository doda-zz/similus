from similus import compare, get_data, compare_data
import ImageFont
import ImageDraw
import ImageChops
import Image
from path import path
from splitter import char_split, center_on_bg

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
    '''Caches both the Image object as well as numpy array in memory'''
    def __init__(self):
        self.images = []

    def load(self, images):
        for image in images:
            self.add(image)

    def add(self, image):
        self.images.append((image, get_data(image)))

    def __len__(self):
        return len(self.images)

    def compare_many(self, image, sort=True):
        '''
        if sort is falsy, a generator is returned and results come in the order
        images were loaded, else a sorted list is returned
        '''
        if not self.images:
            raise IndexError('No images loaded')
        # this stupid conversion has to happen for whatever reason
        image = image.convert('RGB')
        image_data = get_data(image)
        comparisons = ((other_image, compare_data(image_data, other_image_data)) for
                       other_image, other_image_data in self.images)
        if sort:
            return sorted(comparisons, key=lambda x:x[1], reverse=True)
        return comparisons

    def clear(self):
        self.images = []
            
class Otter(object):
    '''OCR'''
    def __init__(self, directory=None, font_size=14, ):
        self.font_size = font_size
        self.comparison_size = (font_size+3, font_size+3)
        self.crab = Crab()
        if directory:
            self.load_images(path(directory).files())

    def create_images(self, font, alphabet, directory):
        font = ImageFont.truetype(font, self.font_size)
        directory = path(directory)
        directory.makedirs_p()
        for char in alphabet:
            img = self.create_char(font, char, directory)
            self.crab.add(img)

    def create_char(self, font, char, directory):
        im_size = (self.font_size*2, self.font_size*2)
        img = Image.new("RGB", im_size, (255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((2, 2), char, (0,0,0), font=font)
        img = autocrop(img, 'white')
        img = center_on_bg(img, self.comparison_size, 'white')
#        img.show()
        img_path = path(directory).joinpath('%05d.png' % ord(char))
        img.save(img_path)
        return img
        #print img_path

    def load_images(self, image_file_paths):
        for p in image_file_paths:
            self.load_image(p)

    def load_image(self, img_path):
        img = Image.open(img_path)
        self.crab.add(img)

    def ocr(self, img):
        return ''.join(self.ocr_char(center_on_bg(im, self.comparison_size, 'white')) for im in char_split(img))

    def ocr_char(self, img):
        rankings = self.crab.compare_many(img)
        fpath = path(rankings[0][0].filename)
        return unichr(int(fpath.namebase))
            
if __name__ == '__main__':
    import string
    alphabet = string.letters + string.digits
    otter = Otter()
    otter.create_images('/home/ddd/Dropbox/prog/sc2wow/bl.ttf', alphabet=alphabet, directory='similus_images')
    otter = Otter('similus_images')
    print otter.ocr(Image.open('/home/ddd/pr/sc2wow/img/liq.png'))
