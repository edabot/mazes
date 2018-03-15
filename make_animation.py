import imageio
import os

def MakeAnimation(filenames, moviename, fps=10):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('./exports/' + moviename, images, fps=fps)
    for filename in filenames:
        os.remove(filename)
