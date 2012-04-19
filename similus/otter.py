import ImageFont
import ImageDraw
import Image
from path import path
from core import Crab
from splitter import char_split, center_on_bg

class Otter(object):
    '''OCR'''
    def __init__(self, directory=None, font_size=14):
        self.font_size = font_size
        self.comparison_size = (font_size, font_size+2)
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
        img_path = path(directory).joinpath('%05d.png' % ord(char))
        img.save(img_path)
        return img

    def load_images(self, image_file_paths):
        for p in image_file_paths:
            self.load_image(p)

    def load_image(self, img_path):
        img = Image.open(img_path)
        self.crab.add(img)

    def ocr(self, img):
        split = char_split(img)
        print len(split)
        return ''.join(self.ocr_char(center_on_bg(im, self.comparison_size, 'white')) for im in split)

    def ocr_char(self, img):
        rankings = self.crab.compare_many(img)
        lowest = rankings[2][1]
        alls = []
        for i,r in enumerate(rankings[:3]):
            fpath = path(r[0].filename)
            perc = (r[1]/lowest * 100) - 100
            print i, unichr(int(fpath.namebase)), perc, '%'
            alls.append(perc)
        ab = alls[0] - alls[1]
        percss.append(ab)
        print ab
        print 
        fpath = path(rankings[0][0].filename)
        return unichr(int(fpath.namebase))

percss = []
            
if __name__ == '__main__':
    import string
    alphabet = string.letters + string.digits
    otter = Otter()
    otter.create_images('/home/ddd/Dropbox/prog/sc2wow/bl.ttf', alphabet=alphabet, directory='similus_images')
    otter = Otter('similus_images')
    res = []
    for img in path('tests').files():
        res.append(otter.ocr(Image.open(img)))
    print res
    print float(sum(percss))/len(percss)
