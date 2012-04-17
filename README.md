# similus

Similus allows you to easily compute the similarity between 2 images

* Caching of internal data structure for fast comparison of one to many
* Rudimentary OCR


```python
>>> import Image
>>> import similus
>>> im1, im2 = Image.open('im1.jpg'), Image.open('im2.jpg')
>>> if similus.compare(im1, im2) < 100:
>>>     print "Images very dissimilar"
```

## Crab allows you to cache images internally for lotsa comparisons

```python
>>> im3 = Image.open('im3.jpg')
>>> crab = similus.Crab([im1])
>>> crab.add(im2)
>>> 'compare im3 to im1 and im2'
>>> crab.similarities(im3)
((im2, 232.3311), (im1, 193.1231))
>>> len(crab)
2
>>> crab.clear()
>>> len(crab)
0
```

## Basic OCR

If you have the font and can crop to single words (or even better single characters), Otter will automatically create

```python
>>> import string
>>> alphabet = string.letters + string.digits
>>> otter = similus.Otter()
>>> otter.create_images('arial.ttf', alphabet=alphabet, directory='similus_images')
>>> otter.ocr(im1)
u'Shake dat booty'
>>> 'We can load images after the fact'
>>> otter = None
>>> otter = similus.Otter('similus_images')
>>> otter.ocr(im1)
u'Shake dat booty'
```