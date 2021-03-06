from utils import *
import numpy as np
from PIL import Image
from scipy import ndimage


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

    if param['vertical_switch'] and random.randint(0,1):
        # top go bottom and bottom go top
        X = flipAxis(X, 0)
        Y[0] , Y[2] = Y[2] , Y[0]

    # if param['width_shift_range'] and random.randint(0,1):
    #     X = widthShiftRange(X, 0)
    #
    # if param['height_shift_range'] and random.randint(0,1):
    #      X = heightShiftRange(X, 0)

    if param['rotate'] and random.randint(0,1):
         X = rotateImage(X)

    ### uncomment or comment the following 4 lines to save or not images ###
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


def widthShiftRange(X, convolution_size):
    """
        param : image X ,size of the convolution filter
        function : if X has column with only zero on its left and right borders, the function has a probability to move the image and labels on left or right
                   It takes into account a convolution_size by keeping at least convolution/2 columns with zeros on left and right
        return : new image
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
    return X

def heightShiftRange(X,convolution_size):
    """
        param : image X ,size of the convolution filter
        function : if X has column with only zero on its top and bottom borders, the function has a probability to move the image and labels up or down
                   It takes into account a convolution_size by keeping at least convolution/2 rows with zeros on top and bottom
        return : new image
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
    # move down
    else:
        # same but move down
        bottom_pixels = X[len(X)-1-border_size,:]
        while np.sum(bottom_pixels) == 0:
            nb_black_rows += 1
            bottom_pixels = X[len(X)-1-nb_black_rows-border_size,:]
        nb_move = random.randint(0,nb_black_rows)
        X = np.roll(X,nb_move, axis = 0)
        X[:nb_move,:] = 0
    return X


def rotateImage(X):
    """
        param : image X
        function : Generate a random angle between -10 and 10 degrees, and rotate the image and its labels
        return : new image and labels
    """
    angle_degree = random.randint(-10,10)
    X = ndimage.rotate(X,angle_degree,reshape=False)
    return X

# imgpil = Image.open("../../../DATA/data/training/reduced_images/sunhl-1th-02-Jan-2017-162 A AP.jpg")
# img = np.array(imgpil, dtype = 'float')
# imgpil_2 = Image.open("../../../DATA/data/training/reduced_images/sunhl-1th-06-Jan-2017-181 A AP.jpg")
# img_2 = np.array(imgpil_2, dtype = 'float')
#
# temporary_tab = np.zeros(img.shape, dtype = 'float')
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         img[i][j] = img[i][j] + 1
#         temporary_tab[i][j] = np.log(img[i][j])
#
# max = np.amax(temporary_tab)
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         temporary_tab[i][j] = temporary_tab[i][j] / max
#         img[i][j] = temporary_tab[i][j] * 255
#
# fig = plt.figure(figsize=(16,9))
# grid = plt.GridSpec(2, 2)
# img_1_log = fig.add_subplot(grid[0,0])
# img_1_log.imshow(img,cmap='gray')
#
# imgpil = Image.open("../../../DATA/data/training/reduced_images/sunhl-1th-02-Jan-2017-162 A AP.jpg")
# img = np.array(imgpil, dtype = 'float')
#
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         img[i][j] = img[i][j]/255
#         temporary_tab[i][j] = np.exp(img[i][j])
#
# max = np.amax(temporary_tab)
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         temporary_tab[i][j] = temporary_tab[i][j] / max
#         img[i][j] = temporary_tab[i][j] * 255
#
# img_1_exp = fig.add_subplot(grid[0,1])
# img_1_exp.imshow(img,cmap='gray')
#
# temporary_tab = np.zeros(img_2.shape, dtype = 'float')
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         img_2[i][j] = img_2[i][j] + 1
#         temporary_tab[i][j] = np.log(img_2[i][j])
#
# max = np.amax(temporary_tab)
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         temporary_tab[i][j] = temporary_tab[i][j] / max
#         img_2[i][j] = temporary_tab[i][j] * 255
#
# img_2_log = fig.add_subplot(grid[1,0])
# img_2_log.imshow(img_2,cmap='gray')
#
# imgpil_2 = Image.open("../../../DATA/data/training/reduced_images/sunhl-1th-06-Jan-2017-181 A AP.jpg")
# img_2 = np.array(imgpil_2, dtype = 'float')
#
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         img_2[i][j] = img_2[i][j]/255
#         temporary_tab[i][j] = np.exp(img_2[i][j])
#
# max = np.amax(temporary_tab)
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         temporary_tab[i][j] = temporary_tab[i][j] / max
#         img_2[i][j] = temporary_tab[i][j] * 255
#
# img_2_exp = fig.add_subplot(grid[1,1])
# img_2_exp.imshow(img_2,cmap='gray')
#
# fig.savefig("fig_exp.png")
# plt.close()

# imgpil_2 = Image.open("../../../DATA/data/training/reduced_images/sunhl-1th-06-Jan-2017-181 A AP.jpg")
# img_2 = np.array(imgpil_2, dtype = 'float')
#
# labels = loadPointsLandmarks("../../../DATA/labels/training/final_landmarks.csv", "../../../DATA/labels/training/filenames.csv")
# label = labels[27]
# plotLandmarksOnImage(img_2,label,True,"test.png")
#img = np.array(imgpil)
# imgpil_map = Image.open("../../../DATA/labels/training/distance_map/sunhl-1th-02-Jan-2017-162 A AP.jpg")
# img_map = np.array(imgpil_map, dtype = 'float')
# for i in range(1,img.shape[0]-1):
#     for j in range(1,img.shape[1]-1):
#         n = (img[i][j-1]-img[i][j+1]) * (img[i][j-1]-img[i][j+1]) + (img[i-1][j]-img[i+1][j]) * (img[i-1][j]-img[i+1][j])
#         if (n < 50):
#             img[i-1][j-1] = 255
#         else :
#             img[i-1][j-1] = 0
# fig = plt.figure(figsize=(16,9))
# grid = plt.GridSpec(1, 2)
# ax_img_exp = fig.add_subplot(grid[0,0])
# ax_img_exp.imshow(img,cmap='gray')
# ax_img_exp_div = fig.add_subplot(grid[0,1])
# ax_img_exp_div.imshow(img,cmap='gray')
# fig.savefig("fig_exp.png")
# plt.close()
