import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt, pi
from distance_map import *
from PIL import Image
import os

def generateTrainingAndValidSetsCSV(percent_training, exp_name):
    """
        params : percent of files that you want to use as training files, the name of the experience
        function : read the filenames that are used for the experience and create 2 set : valid and training
                   it creates 2 csv containing the filenames for both sets
        return : zero
    """
    list_filenames_df = pd.read_csv("../../../DATA/labels/training_distance_map/filenames.csv")
    training_files_df = pd.DataFrame(columns = ["Index", 'Name'])
    validation_files_df = pd.DataFrame(columns = ["Index", 'Name'])

    os.makedirs(os.path.join('../../../Results/Distance_map_prediction/',exp_name,'Sets'))

    t = 0
    v = 0
    for index, row in list_filenames_df.iterrows():
        if random.uniform(0,1) < percent_training:
            training_files_df.loc[t,"Index"]=index
            training_files_df.loc[t,"Name"]=row['Name']
            t += 1
        else:
            validation_files_df.loc[v,'Index']=index
            validation_files_df.loc[v,'Name']=row['Name']
            v += 1

    training_files_df.to_csv(r'../../../Results/Distance_map_prediction/'+exp_name+'/Sets/training_files.csv',index = None, header = True)
    validation_files_df.to_csv(r'../../../Results/Distance_map_prediction/'+exp_name+'/Sets/validation_files.csv',index = None, header = True)

"""
Function which allows to load data from the csv file sent by organizers, here data are the training or test images
:param path_csv: path to csv file
:param images_path: path where all images are stored
:param nb_images: number of images that we want to load, the default value is the whole data set
:return images: list of images extracted from csv file
"""
def loadImagesModified(path_csv, path_images, nb_images = None):
    images = []
    name_images = []
    dataframe_names_images = pd.read_csv(path_csv)

    if (nb_images == None):
        for index_names in range(len(dataframe_names_images)):
            img = mpimg.imread(path_images + dataframe_names_images.iloc[index_names].iloc[0].split('.')[0] + '.png')
            name_images.append(dataframe_names_images.iloc[index_names].iloc[0])
            images.append(img)
    else :
        if (nb_images > len(dataframe_names_images)):
            print("Not enough images in the database, loading of all images")
            loadImagesModified(path_csv, path_images)

        else :
            counter = 0

            while(counter < nb_images):
                img = mpimg.imread(path_images + dataframe_names_images.iloc[counter].iloc[0])
                images.append(img)
                name_images.append(dataframe_names_images.iloc[counter].iloc[0])
                counter += 1

    return(name_images, images)

"""
Function which allows to load data from a csv file, created by Benjamin with function generateTrainingAndValidSetsCSV, here data are the training or test images
:param save_images_path: path where all images are stored
:param index_dataframe_path: path to csv file which contains the index and the names of the images to load
:param nb_images: number of images that we want to load, the default value is the whole data set
:return images: list of images extracted from csv file
"""
def loadImages(index_dataframe_path, images_path, nb_images = None):
    dataframe_numbers_lines = pd.read_csv(index_dataframe_path)
    images = []
    if (nb_images == None):
        for index, row in dataframe_numbers_lines.iterrows():
            img = mpimg.imread(images_path+ row['Name'].split('.')[0] + '.png')
            img = np.array(img, dtype = 'float')
            img = img.reshape(img.shape[0], img.shape[1], 1)
            images.append(img)

    else :
        if (nb_images > len(dataframe_numbers_lines)):
            print("Not enough images in the database, loading of all images")
            loadImages(index_dataframe_path, images_path)

        else :
            counter = 0

            while(counter < nb_images):
                img = mpimg.imread(images_path + dataframe_numbers_lines.iloc[counter].iloc[0])
                img = np.array(img, dtype = 'float')
                img = img.reshape(img.shape[0], img.shape[1], 1)
                images.append(img)
                counter += 1

    images = np.array(images, dtype = 'float')
    return(images)


def loadGTs(index_dataframe_path, images_path_1,nb_images = None):
    dataframe_numbers_lines = pd.read_csv(index_dataframe_path)
    images = []
    if (nb_images == None):
        for index, row in dataframe_numbers_lines.iterrows():
            name = row['Name']
            name = name.split('.')[0] + '.png'

            img1 = Image.open(images_path_1 + name)
            img1 = np.array(img1, dtype = 'float')
            img1 = img1.reshape(img1.shape[0], img1.shape[1], 1)

            # img2 = Image.open(images_path_2 + name)
            # img2 = np.array(img2, dtype = 'float')
            # img2 = img2.reshape(img2.shape[0], img2.shape[1], 1)
            #
            # img3 = [img1, img2]

            images.append(img1)

    else :
        if (nb_images > len(dataframe_numbers_lines)):
            print("Not enough images in the database, loading of all images")
            loadGTS(index_dataframe_path, images_path_1 , images_path_2)

        else :
            counter = 0

            while(counter < nb_images):
                name = dataframe_numbers_lines.iloc[counter].iloc[0]
                name = name.split('.')[0] + '.png'

                img1 = mpimg.imread(images_path_1 + name)
                img1 = np.array(img, dtype = 'float')
                img1 = img1.reshape(img1.shape[0], img1.shape[1], 1)

                img2 = Image.open(images_path_2 + name)
                img2 = np.array(img2, dtype = 'float')
                img2 = img2.reshape(img2.shape[0], img2.shape[1], 1)

                images[0].append(img1)
                images[1].append(img2)

                counter += 1

    images = np.array(images, dtype = 'float')
    return(images)


def loadAngles(filenames_path,filenames_validation_path,labels_path):

    filenames_df = (pd.read_csv(filenames_path)).values
    validation_files_df = (pd.read_csv(filenames_validation_path)).values
    angles_df = (pd.read_csv(labels_path)).values
    angles = []
    for filename in validation_files_df:
        row_number = np.where(filenames_df == validation_files_df)[0][0]
        angles.append(angles_df[row_number])
    angles = np.array(angles)
    return angles

def loadContrastedImages(index_dataframe_path, images_path, dark_images_path, light_images_path, nb_images = None):
    images = []
    dataframe_numbers_lines = pd.read_csv(index_dataframe_path)

    if (nb_images == None):
        for index, row in dataframe_numbers_lines.iterrows():

            img = mpimg.imread(images_path + row['Name'])
            img = np.array(img, dtype = 'float')

            img_dark = mpimg.imread(dark_images_path + row['Name'])
            img_dark = np.array(img_dark, dtype = 'float')

            img_light = mpimg.imread(light_images_path + row['Name'])
            img_light = np.array(img_light, dtype = 'float')

            img_merge = np.zeros((img.shape[0], img.shape[1], 3))

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    img_merge[i][j] = img[i][j]
                    img_merge[i][j][1] = img_dark[i][j]
                    img_merge[i][j][2] = img_light[i][j]

            images.append(img_merge)

    else :
        if (nb_images > len(dataframe_numbers_lines)):
            print("Not enough images in the database, loading of all images")
            loadContrastedImages(index_dataframe_path, images_path, dark_images_path, light_images_path)

        else :
            counter = 0

            while(counter < nb_images):
                img = mpimg.imread(images_path + dataframe_numbers_lines.iloc[counter].iloc[0])
                img = np.array(img, dtype = 'float')

                img_dark = mpimg.imread(dark_images_path + dataframe_numbers_lines.iloc[counter].iloc[0])
                img_dark = np.array(img_dark, dtype = 'float')

                img_light = mpimg.imread(light_images_path + dataframe_numbers_lines.iloc[counter].iloc[0])
                img_light = np.array(img_light, dtype = 'float')

                img_merge = np.zeros((img.shape[0], img.shape[1], 3))

                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        img_merge[i][j] = img[i][j]
                        img_merge[i][j][1] = img_dark[i][j]
                        img_merge[i][j][2] = img_light[i][j]

                images.append(img_merge)

                counter += 1

    images = np.array(images,dtype='float')

    return(images)

def loadPointsLandmarks(path, index_dataframe_path):
    labels = []

    dataframe_numbers_lines = pd.read_csv(index_dataframe_path)
    df = pd.read_csv(path)
    length = len(df.iloc[0])/2
    for index, row in dataframe_numbers_lines.iterrows():
        label = []
        for i in range(length):
            label.append(df.iloc[index].iloc[i])
            label.append(df.iloc[index].iloc[i + length])
        labels.append(label)
    return (labels)

def sortMiddleLandmarks(middle_landmarks):

    number_vertebra = len(middle_landmarks)/2
    for i in range(number_vertebra,1,-1):
        for j in range(i-1):
            if middle_landmarks[j+number_vertebra]<middle_landmarks[j+1+number_vertebra]:
                new_y = middle_landmarks[j+number_vertebra]
                middle_landmarks[j+number_vertebra]= middle_landmarks[j+1+number_vertebra]
                middle_landmarks[j+1+number_vertebra] = new_y
                new_x = middle_landmarks[j]
                middle_landmarks[j] = middle_landmarks[j+1]
                middle_landmarks[j+1] = new_x
    return middle_landmarks

def loadDistanceMap(index_dataframe_path, images_path, nb_images = None):
    dataframe_numbers_lines = pd.read_csv(index_dataframe_path)
    images = []
    if (nb_images == None):
        for index, row in dataframe_numbers_lines.iterrows():
            name = row['Name']
            name = name.split('.')[0] + '.png'
            img = mpimg.imread(images_path+ name)
            img = np.array(img, dtype = 'float')
            img = img.reshape(img.shape[0], img.shape[1], 1)
            images.append(img)

    else :
        if (nb_images > len(dataframe_numbers_lines)):
            print("Not enough images in the database, loading of all images")
            loadImages(index_dataframe_path, images_path)

        else :
            counter = 0

            while(counter < nb_images):
                name = dataframe_numbers_lines.iloc[counter].iloc[0]
                name = name.split('.')[0] + '.png'
                img = mpimg.imread(images_path + name)
                img = np.array(img, dtype = 'float')
                img = img.reshape(img.shape[0], img.shape[1], 1)
                images.append(img)
                counter += 1

    images = np.array(images, dtype = 'float')
    return(images)


def normalize(set):
    """
        param : a set of images
        function : normalize each image by dividing each of its pixels by the max value
        return : the normalized set
    """
    for i in range(len(set)):
        set[i] /= float(np.amax(set[i]))
    return set

def test(name_fct, images_path, save_path, labels_path = None, normalize = False):
    index = 0
    for image in os.listdir(images_path):
        print("IMAGE")
        print(image)
        print(index)
        imgpil = Image.open(os.path.join(images_path, image))
        name = image.split(".", 1)[0] + ".png"
        if (labels_path != None):
            imgpil2 = Image.open(os.path.join(labels_path, name))
            img2 = np.array(imgpil2, dtype = 'float')

        img = np.array(imgpil, dtype = 'float')

        if (normalize):
            max_img = np.amax(img)
            img = img/max_img

        if (name_fct == "dark"):
            img = darkImage(img)

        elif (name_fct == "light"):
            img = lightImage(img)

        elif (name_fct == "oldGaussian"):
            img = oldGaussianNoise(img)

        elif (name_fct == "gaussian"):
            img = gaussianNoise(img, img2)

        if (normalize):
            img = img * max_img

        img = Image.fromarray(img.astype('uint8'))
        img.save(os.path.join(save_path, name + ".png"))
        index += 1
    return(0)
