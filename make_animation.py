import imageio
import os

def MakeAnimation(filenames, moviename):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('./exports/' + moviename, images)
    for filename in filenames:
        os.remove(filename)
