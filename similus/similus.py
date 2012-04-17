import Image
import scipy
from scipy.misc import fromimage
from scipy.signal.signaltools import correlate2d
import warnings
warnings.simplefilter("ignore", scipy.ComplexWarning)

def get_data(i):
    # to grayscale
    data = scipy.inner(fromimage(i), [299, 587, 114]) / 1000.0
    return (data - data.mean()) / data.std()

def compare(im1, im2):
    d1, d2 = (get_data(im) for im in (im1,im2))
    return compare_data(d1, d2)

def compare_data(d1, d2):
    return correlate2d(im1, im2, mode='same').max()

if __name__ == '__main__':
    print compare(Image.open('/home/ddd/pr/sc2wow/races/0/t0.png'), Image.open('/home/ddd/pr/sc2wow/races/1/t1.png'))
    print compare(Image.open('/home/ddd/pr/sc2wow/races/1/t1.png'), Image.open('/home/ddd/pr/sc2wow/races/1/z1.png'))
    
