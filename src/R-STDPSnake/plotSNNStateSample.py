'''
@author: clamesc
'''
import numpy as np
import matplotlib.pyplot as plt

# Input sample
# Fig.4.14

im = np.flipud(np.array([[100., 140., 181.,   70.],
 [  110.,  23.,  18.,   30],
 [  40.,   30.,   30.,   56.],
 [  5.,   50.,   5.,   5.],
 [  5.,   5.,   60.,   5.],
 [  10.,   10.,   10.,   10.],
 [  98.,  55.,  52.,   30.],
 [  112.,  64., 130.,   46.]]).T)

plt.imshow(im, cmap='Greys')
plt.axis('off')
plt.show()