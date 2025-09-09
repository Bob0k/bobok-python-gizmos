import numpy as np
import random
from PIL import Image
from math import cos
from datetime import datetime

start = datetime = datetime.now()

def lininterpolate(min_, max_, t):
    return min_ * (1 - t) + max_ * t

def cosinterpolate(min_, max_, t):
    ft = t * 3.1415926535
    f = (1 - cos(ft)) * 0.5
    return min_ * (1 - f) + max_ * f

def floor3(x):
    if x < 85:
        return 0
    elif x < 170:
        return 128
    else:
        return 255
    
def floor2(x):
    if x < 126:
        return 0
    else:
        return 255
    
def floorcustom(x, threshold):
    if x < threshold:
        return 0
    else:
        return 255
    
def rand():
    return random.randrange(256)

def grad(x,y):
    return int((x / float(WIDTH) + y / float(HEIGHT))/2.0 * 255)

def random_anchors(image, step):
    print ' Randomizing anchor points'
    for x in range(0, WIDTH, step):
        for y in range(0, HEIGHT, step):
            image[x][y] = rand()
            
def interpolate_all(image, step):
    print ' Interpolating horizontals'
    for y in range(0, HEIGHT, step):
        for x in range(0, WIDTH - step, step):
            for t in range(step):
                image[t + x][y] = interpolate(image[x][y],
                                              image[x + step][y],
                                              t / float(step))

    print ' Interpolating verticals'
    for x in range(WIDTH):
        for y in range(0, HEIGHT - step, step):
            for t in range(step):
                image[x][t + y] = interpolate(image[x][y],
                                              image[x][y + step],
                                              t / float(step))

def smooth(image):
    smoothimage = np.empty((WIDTH, HEIGHT))
    print ' Smoothing'
    for x in range(WIDTH):
        smoothimage[x][0] = image[x][0]
        smoothimage[x][HEIGHT-1] = image[x][HEIGHT-1]
    for y in range(HEIGHT):
        smoothimage[0][y] = image[0][y]
        smoothimage[WIDTH-1][y] = image[WIDTH-1][y]
    for x in range(1, WIDTH - 1):
        for y in range(1, HEIGHT - 1):
            corners = (image[x-1][y-1]
                        +image[x-1][y+1]
                        +image[x+1][y-1]
                        +image[x+1][y+1]) / 16.0
            sides = (image[x][y-1]
                        +image[x][y+1]
                        +image[x-1][y]
                        +image[x+1][y]) / 8.0

            smoothimage[x][y] = int(corners + sides + image[x][y] / 4.0)
    image = smoothimage

def floor(image):
    print 'Applying floor function'
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            image[x][y] = floor2(image[x][y])

WIDTH = 2**9 + 1
HEIGHT = WIDTH
seed = 123
interpolates = 'cos'
smothes = 0
step = WIDTH - 1
octaves = 25
to_floor = True

if interpolates == 'cos':
    interpolate = cosinterpolate
elif interpolates == 'lin':
    interpolate = lininterpolate
    
if seed == None:
    seed = random.randrange(1000000)
random.seed(seed)

image = np.zeros((WIDTH, HEIGHT))
images = []
for octave in range(octaves):
    print 'Generating octave #', octave + 1
    images.append(np.ones((WIDTH, HEIGHT)))
    random_anchors(images[-1], step / (octave+1))
    interpolate_all(images[-1], step / (octave+1))
    for i in range(smothes):
        smooth(images[-1])
    image += images[octave] / octaves

if to_floor:
    floor(image)

print 'Saving image'
image = np.stack([image, image, image]).T
img = Image.fromarray(image.astype('uint8'))

def strs(*args):
    temp = ''
    for st in args:
        temp += str(st) + ' '
    return temp[:-1]
filename = strs(WIDTH,
              HEIGHT,
              seed,
              interpolates,
              smothes,
              step,
              octaves)+'.png'
img.save(filename)

print 'Done! Saved as', filename
print 'Image has been generated in', datetime.now() - start
