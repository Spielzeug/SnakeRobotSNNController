import numpy as np
import matplotlib.pyplot as plt

# Input sample modified for better visualization

im = np.flipud(np.array([[100., 140., 181.,   70., 110.,  23.,  18.,   30],
 [  40.,   30.,   30.,   56., 5.,   50.,   43.,   5.],
 [  54.,   50.,   43.,   5., 40.,   30.,   30.,   56.,],
 [  46.,   50.,   43.,   5., 53.,   50.,   43.,   5.],
 [  32.,   35.,   60.,   67., 5.,   35.,   60.,   5.],
 [  10.,   10.,   73.,   10., 10.,   10.,   10.,   10.],
 [  98.,  55.,  52.,   30., 98.,  55.,  52.,   30.],
 [  112.,  64., 130.,   46., 112.,  64., 130.,   46.]]).T)

plt.imshow(im, cmap='Greys')
plt.axis('off')
plt.show()