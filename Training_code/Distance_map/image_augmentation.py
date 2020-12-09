from utils import *
import numpy as np
from math import sqrt, pi
from PIL import Image
from scipy import ndimage
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
    )

def randomTransform(X,Y, param, save_path):
    """
        params : image X , labels Y , a dictionnary that contains the transformation that you want to apply,  save path for images generated by the datagen
        function : apply randomly different transformations on the image and labels
        return : new image and landmarks, with transformation
    """
    X = X.reshape(len(X),len(X[0]))
    Y = Y.reshape(len(Y),len(Y[0]))
    if param['horizontal_switch'] and random.randint(0,1):
        # left go on right, right on left
        X = flipAxis(X, 1)
        Y = flipAxis(Y, 1)

    if param['width_shift_range'] and random.randint(0,1):
        X, Y = widthShiftRange(X, Y, 0)

    if param['height_shift_range'] and random.randint(0,1):
         X, Y = heightShiftRange(X, Y, 0)

    if param['rotate'] and random.randint(0,1):
         X,Y = rotateImage(X,Y)

    if param['light'] and random.randint(0,1):
         X = lightImage(X)

    if param['gaussian'] and random.randint(0,1):
         X = gaussianNoise(X,Y)

    if param['dark'] and random.randint(0,1):
         X = darkImage(X)

    if param['transparency'] and random.randint(0,1):
        X = transparencyNoise(X)

    ### uncomment the following 4 lines to save images ###
    # img = X
    # img = Image.fromarray(img.astype('uint8'))
    # img_name = getNextImgName(save_path)
    # img.save(save_name)

    X = X.reshape(len(X),len(X[0]),1)
    Y = Y.reshape(len(Y),len(Y[0]),1)
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
        while np.sum(left_pixels) == 0.0:
            nb_black_columns += 1
            left_pixels = X[:,border_size+nb_black_columns]
        # we move the image and labels up by a random integer between zero and number of black columns
        nb_move = random.randint(0,nb_black_columns)
        X = np.roll(X, -nb_move)
        Y = np.roll(Y, -nb_move)
        # we replace left columns with zeros
        X[:,len(X[0])-nb_move:] = 0.0
        Y[:,len(Y[0])-nb_move:] = 0.0
    #move right
    else:
        # same but on right
        right_pixels = X[:,(len(X[0]))-1-border_size]
        while np.sum(right_pixels) == 0.0:
            nb_black_columns += 1
            right_pixels = X[:,len(X[0])-1-nb_black_columns-border_size]
        nb_move = random.randint(0,nb_black_columns)
        X = np.roll(X,nb_move)
        Y = np.roll(Y,nb_move)
        X[:,:nb_move] = 0.0
        Y[:,:nb_move] = 0.0
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
        while np.sum(up_pixels) == 0.0:
            nb_black_rows += 1
            up_pixels = X[border_size+nb_black_rows,:]
        # we move the image and labels up by a random integer between zero and number of black rows
        nb_move = random.randint(0,nb_black_rows)
        X = np.roll(X, -nb_move, axis = 0)
        Y = np.roll(Y, -nb_move, axis = 0)
        # we replace bottom rows with zeros
        X[len(X)-nb_move:,:] = 0.0
        Y[len(Y)-nb_move:,:] = 0.0
    # move down
    else:
        # same but move down
        bottom_pixels = X[len(X)-1-border_size,:]
        while np.sum(bottom_pixels) == 0.0:
            nb_black_rows += 1
            bottom_pixels = X[len(X)-1-nb_black_rows-border_size,:]
        nb_move = random.randint(0,nb_black_rows)
        X = np.roll(X,nb_move, axis = 0)
        Y = np.roll(Y,nb_move, axis = 0)
        X[:nb_move,:] = 0.0
        Y[:nb_move,:] = 0.0
    return X, Y


def rotateImage(X, Y):
    """
        param : image X , labels Y
        function : Generate a random angle between -10 and 10 degrees, and rotate the image and its labels
        return : new image and labels
    """
    angle_degree = random.randint(-10,10)
    X = ndimage.rotate(X,angle_degree,reshape=False)
    Y = ndimage.rotate(Y,angle_degree,reshape=False)
    return X, Y

def lightImage(X):
    temporary_tab = np.zeros(X.shape, dtype = 'float')
    max = np.amax(X) + 1
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            X[i][j] = X[i][j] / max
            X[i][j] = X[i][j] * 9
            X[i][j] = X[i][j] + 1
            temporary_tab[i][j] = np.log(X[i][j])

    max = np.amax(temporary_tab)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            temporary_tab[i][j] = temporary_tab[i][j] / max
            X[i][j] = temporary_tab[i][j] * 255
    return(X)

def darkImage(X):
    temporary_tab = np.zeros(X.shape, dtype = 'float')
    max = np.amax(X)
    for i in range(temporary_tab.shape[0]):
        for j in range(temporary_tab.shape[1]):
            X[i][j] = X[i][j] / max
            X[i][j] = X[i][j] * 3
            temporary_tab[i][j] = np.exp(X[i][j]) - 1

    max = np.amax(temporary_tab)
    for i in range(temporary_tab.shape[0]):
        for j in range(temporary_tab.shape[1]):
            temporary_tab[i][j] = temporary_tab[i][j] / max
            X[i][j] = temporary_tab[i][j] * 255

    return(X)

def oldGaussianNoise(X):
    height = X.shape[0]
    width = X.shape[1]

    p_1 = [0, 0]
    p_2 = [height - 1, width - 1]

    while (np.sum(X[p_1[0]]) == 0) :
        p_1[0] += 1

    while (np.sum(X[:,p_1[1]]) == 0) :
        p_1[1] += 1

    while (np.sum(X[p_2[0]]) == 0) :
        p_2[0] -= 1

    while (np.sum(X[:,p_2[1]]) == 0) :
        p_2[1] -= 1

    y = random.randint((p_2[1] - p_1[1]) / 4 + p_1[1] + 20, p_1[1] - 20 + 3 * (p_2[1] - p_1[1]) / 4)
    x = random.randint(p_1[0] + 20, p_2[0] - 20)
    if (x == 0):
        x += 1
    if (y == 0):
        y += 1
    center = [x, y]

    R = min(50, abs(x-p_1[0]), abs(x-p_2[0]))

    max = np.amax(X)
    max_gauss = max - X[x][y]

    # x = float(x)
    # y = float(y)
    sigma = 0.3
    # gaussian_matrix = np.zeros((p_2[0] - p_1[0], p_2[1] - p_1[1]))
    gaussian_matrix = np.zeros((2*R, width))
    # for i in range(gaussian_matrix.shape[0]):
    #     for j in range(gaussian_matrix.shape[1]):
    #         gaussian_matrix[i][j] =  max_gauss * np.exp(-10 * (((float(i - (x - p_1[0])) / sqrt(x**2 + y**2))**2 + ((float(j - (y - p_1[1]))) / sqrt(x**2 + y**2))**2) / (2 * sigma**2)))
    #         X[i + p_1[0]][j + p_1[1]] += gaussian_matrix[i][j]
    #         if (X[i + p_1[0]][j + p_1[1]] > 255):
    #             X[i + p_1[0]][j + p_1[1]] = 255
    for i in range(x-R,x+R):
        for j in range(width):
            gaussian_matrix[i - x + R][j] =  max_gauss * np.exp(-40 * (((float(abs(i - x)) / sqrt(x**2 + y**2))**2 + ((float(abs(j - y))) / sqrt(x**2 + y**2))**2) / (2 * sigma**2)))
            X[i][j] += gaussian_matrix[i - x + R][j]
            if (X[i][j] > max):
                X[i][j] = max
    return(X)

def gaussianNoise(X, Y):
    height = X.shape[0]
    width = X.shape[1]

    p_1 = [0, 0]
    p_2 = [height - 1, width - 1]

    while (np.sum(X[p_1[0]]) == 0) :
        p_1[0] += 1

    while (np.sum(X[:,p_1[1]]) == 0) :
        p_1[1] += 1

    while (np.sum(X[p_2[0]]) == 0) :
        p_2[0] -= 1

    while (np.sum(X[:,p_2[1]]) == 0) :
        p_2[1] -= 1

    nb_noise = random.randint(0,1)
    max_X = np.amax(X)
    max_Y = np.amax(Y)

    if (nb_noise) :
        x1 = random.randint(p_1[0], height/2)
        while (sum(Y[x1]) == 0):
            x1 = random.randint(p_1[0], height/2)
        column_aux = 0
        while (Y[x1][column_aux] == 0):
            column_aux +=1
        column_aux += int(sum(Y[x1]/max_Y)/2)
        y1 = random.randint(column_aux - 10, column_aux + 10)


        x2 = random.randint(height/2, p_2[0])
        while (sum(Y[x2]) == 0):
            x2 = random.randint(height/2, p_2[0])
        column_aux = 0
        while (Y[x2][column_aux] == 0):
            column_aux +=1
        column_aux += int(sum(Y[x2]/max_Y)/2)
        y2 = random.randint(column_aux - 10, column_aux + 10)

        if (x1 == 0):
            x1 += 1
        if (y1 == 0):
            y1 += 1
        center1 = [x1, y1]

        R1 = min(50, abs(x1-p_1[0]))
        R2 = min(50, abs(x2-p_2[0]))
        R = min(R1, R2)

        max_gauss1 = max_X - X[x1][y1]
        max_gauss2 = max_X - X[x2][y2]

        sigma = 0.3

        gaussian_matrix = np.zeros((2*R, width))

        for i in range(2*R):
            for j in range(width):
                gaussian_matrix[i][j] =  max_gauss1 * np.exp(-50 * (((float(i - R) / sqrt(x1**2 + y1**2))**2 + ((float(abs(j - y1))) / sqrt(x1**2 + y1**2))**2) / (2 * sigma**2)))
                X[i + x1 - R][j] += gaussian_matrix[i][j]
                if (X[i + x1 - R][j] > max_X):
                    X[i + x1 - R][j] = max_X
                gaussian_matrix[i][j] =  max_gauss2 * np.exp(-50 * (((float(i - R) / sqrt(x2**2 + y2**2))**2 + ((float(abs(j - y2))) / sqrt(x2**2 + y2**2))**2) / (2 * sigma**2)))
                X[i + x2 - R][j] += gaussian_matrix[i][j]
                if (X[i + x2 - R][j] > max_X):
                    X[i + x2 - R][j] = max_X

    else :
        x1 = random.randint(p_1[0], p_2[0])
        while (sum(Y[x1]) == 0):
            x1 = random.randint(p_1[0], p_2[0])
        column_aux = 0
        while (Y[x1][column_aux] == 0):
            column_aux +=1
        column_aux += int(sum(Y[x1]/max_Y)/2)
        y1 = random.randint(column_aux - 10, column_aux + 10)

        if (x1 == 0):
            x1 += 1
        if (y1 == 0):
            y1 += 1
        center1 = [x1, y1]

        R = min(50, abs(x1-p_1[0]), abs(x1-p_2[0]))

        max_gauss1 = max_X - X[x1][y1]

        sigma = 0.3

        gaussian_matrix = np.zeros((2*R, width))

        for i in range(2*R):
            for j in range(width):
                gaussian_matrix[i][j] =  max_gauss1 * np.exp(-50 * (((float(i - R) / sqrt(x1**2 + y1**2))**2 + ((float(abs(j - y1))) / sqrt(x1**2 + y1**2))**2) / (2 * sigma**2)))
                X[i + x1 - R][j] += gaussian_matrix[i][j]
                if (X[i + x1 - R][j] > max_X):
                    X[i + x1 - R][j] = max_X
    return(X)

def transparencyNoise(X):
    img_contour = Image.fromarray(X.astype('uint8'))
    img_contour = imgpil.filter(CONTOUR)
    img_contour = np.array(img_contour)

    height = X.shape[0]
    width = X.shape[1]

    p_1 = [0, 0]
    p_2 = [height - 1, width - 1]

    while (np.sum(X[p_1[0]]) == 0) :
        p_1[0] += 1

    while (np.sum(X[:,p_1[1]]) == 0) :
        p_1[1] += 1

    while (np.sum(X[p_2[0]]) == 0) :
        p_2[0] -= 1

    while (np.sum(X[:,p_2[1]]) == 0) :
        p_2[1] -= 1

    line_1 = random.randint(p_1[0], 9*height/10)
    line_2 = line_1 + 50
    column_1 = random.randint(width/3, width/2)
    column_2 = column_1 + 40
    # column = 0
    # while (column < width - 1 and Y[line_1][column] == 0):
    #     column += 1
    # column_1 = column
    # while (column < width - 1 and Y[line_1][column] != 0):
    #     column += 1
    # column_2 = column
    # column = 0
    # while (column < width - 1 and Y[line_2][column] == 0):
    #     column += 1
    # column_3 = column
    # while (column < width - 1 and Y[line_2][column] != 0):
    #     column += 1
    # column_4 = column
    #
    # column_1 = min(column_1, column_2, column_3, column_4)
    # column_2 = max(column_1, column_2, column_3, column_4)

    val = np.mean(X[line_1:line_2, column_1:column_2])

    for i in range (line_1, line_2 + 1):
        for j in range (column_1, column_2 + 1):
            # if (X[i][j] > val):
            if (img_contour[i][j] != 255):
                # X[i][j] = val
                # X[i][j] = (X[i-1][j-1] + X[i-1][j] + X[i-1][j+1] + X[i][j-1] + X[i][j+1] + X[i+1][j-1] + X[i+1][j] + X[i+1][j+1] + X[i][j])/9
                x = random.randint(-10,10)
                y = random.randint(-10,10)
                while (j+y >= width):
                    y = random.randint(-10,10)
                while (i+x >= height):
                    x = random.randint(-10,10)
                X[i][j] = X[i+x][j+y]
    return(X)

def RGBAImage(X):
    new_image = np.zeros((X.shape[0], X.shape[1], 4))
    for i in range (X.shape[0]):
        for j in range (X.shape[1]):
            new_image[i][j][0] = X[i][j]
            new_image[i][j][1] = X[i][j]
            new_image[i][j][2] = X[i][j]
            new_image[i][j][3] = 0
    return(new_image)

def removeNoise(source_path,save_path):
    height_filter = 70
    width_filter = 20
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for image in os.listdir(source_path):
        print(image)
        imgpil = Image.open(os.path.join(source_path, image))
        img = np.array(imgpil, dtype = "float")
        img = (img > 10)*img
        i = height_filter
        while i < img.shape[0]-height_filter:
            j = width_filter
            while j < img.shape[1]-width_filter:
                if (sum(img[i-height_filter : i+height_filter , j-width_filter]) + sum(img[i-height_filter : i+height_filter , j+width_filter]) == 0):
                    if (sum(img[i-height_filter, j-width_filter: j+width_filter]) == 0 and sum(img[ i+height_filter, j-width_filter: j+width_filter]) == 0):
                        img[i-height_filter : i+height_filter, j-width_filter : j+width_filter] = np.zeros((2*height_filter, 2*width_filter))
                        j += 2*width_filter-1
                    else:
                        j +=1
                else:
                    j += 1
            i += 1

        imgpil = Image.fromarray(img.astype('uint8'))
        imgpil.save(save_path + image)

# removeNoise("../../../DATA/labels/training_angles/1024_256/final","../../../DATA/labels/training_angles/1024_256/final_improved/")