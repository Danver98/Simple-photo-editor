
import sys
from PIL import ImageQt , Image , ImageFilter , ImageOps
import matplotlib.pyplot as plt , numpy as np
from skimage.util import random_noise

box_blur_radius = 0

def copy(src ,dest):
    with open(src, 'rb') as src_image:
        with open(dest ,'wb') as dest_image:
            dest_image.write(src_image.read())

def histogram(image):
    try:
        r,g,b = image.split()

        """
        plt.plot(r.histogram() , label = "Красные пиксели", color="red")
        plt.plot(g.histogram(), label = "Зелёные пиксели" , color = "green")
        plt.plot(b.histogram(), label = "Синие пиксели", color="blue")
        plt.title("Гистограмма")
        plt.legend()
        plt.show()
        """
        fig, axis = plt.subplots(3 , sharex = True , sharey = True)
        fig.suptitle('Гистограмма изображения')
        axis[0].plot(r.histogram() , label = "Красные пиксели", color="red")
        axis[1].plot(g.histogram(), label = "Зелёные пиксели" , color = "green")
        axis[2].plot(b.histogram(), label = "Синие пиксели", color="blue")
        fig.canvas.set_window_title("Гистограмма")
        plt.show()
    except ValueError as e:
        return -1

def transpose(image , method):
    return image.transpose(method)

def rotate(image , angle):
    return image.rotate(angle)

def scale(image , coeff):
    pass

def get_recalculated_sizes( width , height , auto_width = False, auto_height = False):
    if(auto_width):
        new_height = height
        new_width = int(new_height * width/height)
    elif (auto_height):
            new_width = width
            new_height = int(new_width * height/width)
    else:
        new_width = width
        new_height = height
    return (new_width , new_height)

def get_ratio_height(width, height, r_width):
    return int(r_width/width*height)

def get_ratio_width(width, height, r_height):
    return int(r_height/height*width)

def resize(image, new_width , new_height):
    return image.resize((new_width , new_height) , Image.ANTIALIAS)

def noise(image, *params):
    im_arr = np.asarray(image)
    noise_img = random_noise(im_arr, mode='gaussian' , var=0.5**2)
    noise_img =(255*noise_img).astype(np.uint8)
    img = Image.fromarray(noise_img)
    return img

def blur(image , *params):
    return image.filter(ImageFilter.BLUR)

def invert(image , *params):
    return ImageOps.invert(image)

def greyscale(image, *params):
    return image.convert('L')

def smooth(image , *params):
    return image.filter(ImageFilter.SMOOTH)

def sharpen(image , *params):
    return image.filter(ImageFilter.SHARPEN)

def smooth_more(image , *params):
    return image.filter(ImageFilter.SMOOTH_MORE)

def gaussian_blur(image , *params):
    return image.filter(ImageFilter.GaussianBlur)

def emboss(image, *params):
    return image.filter(ImageFilter.EMBOSS)

def find_edges(image , *params):
    return image.filter(ImageFilter.FIND_EDGES)


def box_blur(image, *params):
    global box_blur_radius
    if(not box_blur_radius):
        box_blur_radius = 0
    box_blur_radius+=2
    print("From box blur")
    return image.filter(ImageFilter.BoxBlur(box_blur_radius))

"""
self.menuFilters.setEnabled(False)
        self.menuOther.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.btnRotateLeft.setEnabled(False)
        self.btnRotateRight.setEnabled(False)
        self.btnHistogram.setEnabled(False)
        self.btnResize.setEnabled(False)
        self.checkBoxAutoRatio.setEnabled(False)
"""

if __name__ =='__main__':
    default = "C:/Users/Супемэн/Desktop/2005.09.09-8.JPG"
    image = Image.open(default)
    image.transpose(Image.ROTATE_270).show()
    #image.rotate(180).show()
