# similus

Similus allows you to easily compute the similarity between 2 images

### Features
* Grayscale Image Comparison
* Caching of internals for fast comparison of one to many

```python
>>> import Image
>>> import similus
>>> im1, im2, im3 = Image.open('im1.jpg'), Image.open('im2.jpg'), Image.open('im3.jpg')
>>> similus.compare(im1, im2)
212.231
>>> similus.compare(im2, im3)
123.321
```

## Crab allows you to cache images internally for lotsa comparisons

```python
>>> im3 = Image.open('im3.jpg')
>>> crab = similus.Crab([im1])
>>> crab.add(im2)
>>> 'compare im3 to im1 and im2'
>>> crab.compare_all_to(im3)
((<im2>, 232.3311), (<im1>, 193.1231))
>>> len(crab)
2
>>> crab.clear()
>>> len(crab)
0
```