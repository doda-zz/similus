from similus import compare, get_data, compare_data
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
    '''Caches both the Image object as well as numpy array in memory'''
    def __init__(self, images=None):
        self.images = []
        if isinstance(images, basestring):
            images = path(images).files()
        if images:
            self.load(images)

    def load(self, images):
        for image in images:
            self.add(image)

    def add(self, image):
        self.images.append((image, get_data(image)))

    def __len__(self):
        return len(self.images)

    def compare_all_to(self, image, sort=True):
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
            
