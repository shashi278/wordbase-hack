import numpy as np
import cv2
from PIL import Image

from sklearn.svm import LinearSVC
import pickle

#create simple dict for alphabets
alph_dict= {}
alph_dict_rev= {}
for num, alph in zip(range(1,27),"ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()):
    alph_dict[num]=alph
    alph_dict_rev[alph]=num

def reshape_img(arr):
    """
    param arr: numpy array of an image(thresholded image)

    returns flat_arr: a 1D list containing zeroes and ones
    """
    flat_arr=[]
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i][j][0]== 255:
                flat_arr.append(1)
            else:
                flat_arr.append(0)

    return flat_arr

def create_data(train_img_list, label_list):
    """
    param train_img_list: A list containg images to train model upon
    param label_list: A list containing labels corresponding to images
                      in the train_img_list
    
    returns inp_arr: a ready-to-feed numpy array for training
    returns np.array(label_list): a numpy array of corresponding label_list
    """
    inp_arr=[]

    for img in train_img_list:
        img= cv2.imread(img)
        inp_arr.append(reshape_img(img))
    
    inp_arr= np.array(inp_arr)

    return inp_arr,np.array(label_list)

def triger_create():
    """
    create lists of images and corresponding labels

    returns images: a list containing path to train images
    returns labels: a list containing corres. numeral labels
    """
    images=[]
    labels=[]
    for i in range(1,27):
        for j in range(1,7):
            try:
                img= Image.open("train_images/{}.{}.png".format(i,j))
            except FileNotFoundError:
                continue

            images.append("train_images/{}.{}.png".format(i,j))
            labels.append(i)
    
    return images, labels

# if the trained model already exists then use it
# otherwise train and save one
try:
    with open("svm_model","rb") as file:
        svm_model= pickle.load(file)
except FileNotFoundError:
    in_arr, out_arr= create_data(*triger_create())
    
    svm_model= LinearSVC(
                random_state=43,
                tol=1e-5,
                max_iter=5000,
                verbose=0).fit(in_arr,out_arr)

    with open("svm_model","wb") as file:
        pickle.dump(svm_model,file)
    

if __name__ == "__main__":
    test_img= cv2.imread("train_images/img_118.png")
    pred= svm_model.predict([reshape_img(test_img)])
    print(alph_dict[pred[0]])
