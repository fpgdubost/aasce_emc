from utils import *
import numpy as np
from PIL import Image
from scipy import ndimage
from math import cos, sin

def randomTransform(X,Y, param, save_path):
    """
        params : image X , labels Y , a dictionnary that contains the transformation that you want to apply,  save path for images generated by the datagen
        function : apply randomly different transformations on the image and labels
        return : new image and landmarks, with transformation
    """
    X = X.reshape(len(X),len(X[0]))
    if param['horizontal_switch'] and random.randint(0,1):
        # left go on right, right on left
        X = flipAxis(X, 1)
        for i in range(len(Y)):
            if i%2==0:
                Y[i]=1-Y[i]
    if param['width_shift_range'] and random.randint(0,1):
        X, Y = widthShiftRange(X, Y, 0)
    if param['height_shift_range'] and random.randint(0,1):
         X, Y = heightShiftRange(X, Y, 0)
    if param['rotate'] and random.randint(0,1):
         X,Y = rotateImage(X,Y)

    ### uncomment the following 4 lines to save images ###
    # img = X
    # img = Image.fromarray(img.astype('uint8'))
    # img_name = getNextImgName(save_path)
    # img.save(save_name)

    X = X.reshape(len(X),len(X[0]),1)
    return X,Y


def getNextImgName(path):
    """
        param : the path were images generated by the datagen are saved
        function : compute the name of a new image, according to those which already exist
        return : the name of the new image
    """
    list_img_names_with_extension = os.listdir(path)
    next_img_num = 1
    num = 1
    new_name = 'img_1.png'
    for name_with_extension in list_img_names_with_extension:
        name = name_with_extension.split(".")[0]
        num = int(name.split("_")[1])
        if num >= next_img_num:
            next_img_num = num +1
    new_name = 'img_'+str(next_img_num)+'.png'
    return new_name

def flipAxis(X, axis):
    """
        param : An image X, the axis around wich you want to flip X
        function : flip X around the axis
        return : the flipped image
    """
    X = X.swapaxes(axis,0)
    X = X[::-1, ...]
    X = X.swapaxes(0, axis)
    return X


def widthShiftRange(X, Y, convolution_size):
    """
        param : image X , labels Y , size of the convolution filter
        function : if X has column with only zero on its left and right borders, the function has a probability to move the image and labels on left or right
                   It takes into account a convolution_size by keeping at least convolution/2 columns with zeros on left and right
        return : new image and labels
    """
    border_size = convolution_size/2
    nb_black_columns = 0
    # move left
    if random.randint(0,1):
        #first we count the number of columns that contains only zeros on left
        left_pixels = X[:,border_size]
        while np.sum(left_pixels) == 0:
            nb_black_columns += 1
            left_pixels = X[:,border_size+nb_black_columns]
        # we move the image and labels up by a random integer between zero and number of black columns
        nb_move = random.randint(0,nb_black_columns)
        X = np.roll(X, -nb_move)
        # we replace left columns with zeros
        X[:,len(X[0])-nb_move:] = 0
        for i in range(len(Y)):
            if i%2==0:
                Y[i]=Y[i]-(nb_move/float(len(X[0])))
    #move right
    else:
        # same but on right
        right_pixels = X[:,(len(X[0]))-1-border_size]
        while np.sum(right_pixels) == 0:
            nb_black_columns += 1
            right_pixels = X[:,len(X[0])-1-nb_black_columns-border_size]
        nb_move = random.randint(0,nb_black_columns)
        X = np.roll(X,nb_move)
        X[:,:nb_move] = 0
        for i in range(len(Y)):
            if i%2==0:
                Y[i]=Y[i]+(nb_move/float(len(X[0])))
    return X, Y

def heightShiftRange(X,Y, convolution_size):
    """
        param : image X , labels Y , size of the convolution filter
        function : if X has column with only zero on its top and bottom borders, the function has a probability to move the image and labels up or down
                   It takes into account a convolution_size by keeping at least convolution/2 rows with zeros on top and bottom
        return : new image and labels
    """
    border_size = convolution_size/2
    nb_black_rows = 0
    #move up
    if random.randint(0,1):
        #first we count the number of rows that contains only zeros
        up_pixels = X[border_size,:]
        while np.sum(up_pixels) == 0:
            nb_black_rows += 1
            up_pixels = X[border_size+nb_black_rows,:]
        # we move the image and labels up by a random integer between zero and number of black rows
        nb_move = random.randint(0,nb_black_rows)
        X = np.roll(X, -nb_move, axis = 0)
        # we replace bottom rows with zeros
        X[len(X)-nb_move:,:] = 0
        for i in range(len(Y)):
            if i%2==1:
                Y[i]=Y[i]-(nb_move/float(len(X)))
    # move down
    else:
        # same but move down
        bottom_pixels = X[len(X)-1-border_size,:]
        while np.sum(bottom_pixels) == 0:
            nb_black_rows += 1
            bottom_pixels = X[len(X)-1-nb_black_rows-border_size,:]
        # on deplace l image d'un nombre de colonne aleatoire entre 0 et nb
        nb_move = random.randint(0,nb_black_rows)
        X = np.roll(X,nb_move, axis = 0)
        # on remplace toutes les colonnes de droites par des zeros
        X[:nb_move,:] = 0
        for i in range(len(Y)):
            if i%2==1:
                Y[i]=Y[i]+(nb_move/float(len(X)))
    return X, Y


def rotateImage(X, Y):
    """
        param : image X , labels Y
        function : Generate a random angle between -10 and 10 degrees, and rotate the image and its labels
        return : new image and labels
    """
    angle_degree = random.randint(-10,10)
    angle_radian = angle_degree*np.pi/180
    copy_Y = np.zeros(len(Y))
    for i in range(len(Y)-1):
        if i%2 == 0:
            copy_Y[i] = (Y[i]-0.5)*cos(angle_radian) - (Y[i+1]-0.5)*sin(angle_radian) +0.5
            copy_Y[i+1] = (Y[i]+0.5)*sin(angle_radian) + (Y[i+1]+0.5)*cos(angle_radian) -0.5

    j = 0
    # we count the number of labels which stay in the image
    while j<len(Y) and 0 <= copy_Y[j] and copy_Y[j]<=1:
        j+=1
    # if all the labels are still in the images, we tranform X and Y
    if j == len(copy_Y):
        Y = copy_Y
        X = ndimage.rotate(X,angle_degree,reshape=False)
    return X, Y
