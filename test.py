import numpy as np

ground = [0,0,0]
trees = [0,255,0]
bush = [0,255,0]
towers = [0,0,255]
wires = [0,0,255]
copter = [255,255,255]
cars = [255,0,255]
buildings = [255,255,0]

COLOR_DICT = dict(ground = ground, trees = trees, bush = bush, towers = towers, wires = wires, copter = copter, cars = cars, buildings = buildings)

channels = ['copter', 'copter', 'copter']

rgb_matrix = np.zeros((len(channels),3))
for ch, color in enumerate(channels):
    rgb_matrix[ch] = COLOR_DICT[color]
print(rgb_matrix)
arr = np.array([[[0, 0, 0], [0, 0, 1], [0, 1, 0]], [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0, 0.5]], [[0.5, 0.5, 0], [0.4, 0.4, 0.2], [0.3, 0.2, 0.5]]])
img = np.zeros((3,3,len(channels)))
img[:,:] = np.matmul(arr[:,:],rgb_matrix)
print(img)
"""
img = np.zeros((3,3,3))
msk = np.zeros((3,3,3,3))
arr = np.array([[[0, 0, 0], [0, 0, 1], [0, 1, 0]], [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0, 0.5]], [[0.5, 0.5, 0], [0.4, 0.4, 0.2], [0.3, 0.2, 0.5]]])
#arr = np.moveaxis(arr, -1, 0)
v = np.amax(arr, axis=-1)
i = np.argmax(arr, axis=-1)
print(i)
print(v)
img[:,:] = np.array([255,255,255])*v[:,:]
print(img)
"""
"""

print(cars*True)
#img[:,:] = COLOR_DICT[channels[arr2[:,:]]]
#print(arr2)
for ch, color in enumerate(channels):
    #img[:,:] = COLOR_DICT[color] if (arr2 == ch) else img[:,:]
    msk[:,:,ch] = COLOR_DICT[color]*np.array(arr[:,:,ch], arr[:,:,ch], arr[:,:,ch])
    #img[:,:] = (COLOR_DICT[color]*arr[:,:,ch]).sum(axis=0)
#print(img)
print(msk)
print("-----")
print(img)
"""