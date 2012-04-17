# similus

Similus allows you to easily compute the similarity between 2 images

* Caching of internal data structure for fast comparison of one to many
* Rudimentary OCR


```python
>>> import similus
>>> im1, im2, im3 = Image.open('im1.jpg'), Image.open('im2.jpg'), Image.open('im2.jpg')
>>> if similus.compare(im1, im2) < 100:
>>>     print "Images very dissimilar"

>>> # Crab allows you to cache images internally for lotsa comparisons
>>> crab = similus.Crab([im1])
>>> crab.add(im2)
>>> # compare im3 to im1 and im2
>>> crab.similarities(im3)
((im2, 232.3311), (im1, 193.1231))
>>>len(crab)
2
>>> crab.clear()
>>> len(crab)
0
```