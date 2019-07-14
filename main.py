# -*- coding: utf-8 -*-

from keras.models import Sequential
import numpy as np

x = np.array([[1, 2], [3, 4]])
y = np.sum(x, axis=0)

print(x)
print(y)

model = Sequential()
