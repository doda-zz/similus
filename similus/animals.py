from similus import compare, get_data
import os

class Crab(object):
    def __init__(self):
        self.images = []

    def load(images):
        for image in images:
            self.images.append(get_data(image))

    def __len__(self):
        return len(self.images)

    def compare_many(self, image, sort=True):
        '''
        if sort is falsy, a generator is returned and results come in the order
        images were loaded, else a sorted list is returned
        '''
        if not self.images:
            raise IndexError('No images loaded')
        comparisons = ((other, compare(image, other)) for other in self.images)
        if sort:
            return sorted(comparisons, key=lambda x:x[1])
        return comparisons

    def clear(self):
        self.images = []
            
class Otter(object):
    def __init__(self, directory=None):
        if directory:
            self.load_images(os.listdir(directory))

    def create_images(font, alphabet, directory):
        pass

    def load_images(self, image_files):
        for f in image_files:
            pass
            
