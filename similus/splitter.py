from itertools import groupby
import Image
import ImageEnhance

THRESHOLD = 120

def lows(im):
    '''
    returns for every x value the sum of the 1 darkest pixels
    '''
    pix = im.load()
    get = 1
    return [(x,sum(sorted([pix[x,y] for y in range(im.size[1])])[:get])/float(get)) for x in range(im.size[0])]

def find_chars(im):
    for char, group in groupby(lows(im), lambda x:x[1] < THRESHOLD):
        group = list(group)
        if char:
            # 1 more pixel on each side
            yield group[0][0]-1, group[-1][0]+2

def char_split(im):
    yy = im.size[1]
    return [im.crop((x0, 0, x1, yy)) for x0,x1 in find_chars(im)]

def center_on_bg(im, (newx, newy), bg='white'):
    x,y = im.size
    left = (newx - x) / 2
    top = (newy - y) / 2
    new = Image.new('RGB', (newx, newy), bg)
    new.paste(im, (left, top, left+x, top+y))
    return new

def main():
    i = Image.open('img/liq.png')
#    i.show()
#    low = lows(i)
#    plt.plot(low)
    # false == character
        
#    plt.show()

if __name__ == '__main__':
    main()
