import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

def show_multi_image(imgs):
    nImgs = len(imgs)
    fig=plt.figure(figsize=(nImgs * 10,10))
    nCols = nImgs
    nRows = nImgs // nCols
    for i, v in enumerate(imgs):
        fig.add_subplot(1, nImgs, i + 1)
        plt.imshow(v)
    plt.show()

def show_overlap(img, mask, alpha=0.5):
    fig = Figure(figsize=(10,10))
    canvas = FigureCanvas(fig)
    ax = fig.gca()
    ax.imshow(img)
    ax.imshow(mask, alpha=alpha)
    ax.axis('off')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    canvas.draw()
    width, height = (fig.get_size_inches() * fig.get_dpi()).astype(np.int16)
    image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
    return image