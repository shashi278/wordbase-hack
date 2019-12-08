import cv2
from PIL import Image
from PIL import ImageFilter
import numpy as np
import sys
from collections import Counter

#from train_img_data import img_data_list
from train_img import svm_model, alph_dict, alph_dict_rev, reshape_img

WIDTH = 640/2
HEIGHT = 1136/2


#function to create train images
def create_images(file_path):
	try: 
		main_image = Image.open(file_path)
	except IOError:
		sys.stderr.write("ERROR: Could not open file {}".format(file_path))
		exit(1)

	size = (WIDTH, HEIGHT)
	main_image.thumbnail(size, Image.ANTIALIAS)

	#traverse through the word matrix
	for i in range(13):
		for j in range(10):
			left= j*WIDTH/10
			right= (j+1)*WIDTH/10
			try:
				top= 126+(HEIGHT-126)/13.8*i
			except ZeroDivisionError:
				top= 126+0
			bottom= 126+(HEIGHT-126)/13.8*(i+1)

			pil_image = main_image.crop((left,top,right,bottom))

			opencv_img= pil_to_opencv(pil_image)
			thresh= simple_threshold(opencv_img)

			#check which color is more(b or w?)
			count= Counter(thresh.flatten())
			#print(count)
			if count[0]>count[255]:
				thresh= cv2.bitwise_not(thresh)

			pil_image= opencv_to_pil(thresh)
			pil_image= pil_image.crop((6,8,25,24))
			#opencv_img= pil_to_opencv(pil_image)
			#print(opencv_img.tolist()[:5])
			pil_image.save("train_images/img_{}{}.png".format(i,j))

			#cv2.imshow("train_images/img_{}{}.png".format(i,j),opencv_img)

def unique_count(a):
	colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
	return colors[count.argmax()]

#get the grid from a screenshot image
def get_grid(file_path):
	"""
	params
	======
	file_path: path of the image file

	returns
	=======
	grid: derived letter grid from the image
	blue: list of locaions containing positions of blue letters
	orange: list of locaions containing positions of orange letters
	"""
	img_arr=[]
	grid=[]
	blue=[]
	orange=[]

	try: 
		main_image = Image.open(file_path)
	except IOError:
		sys.stderr.write("ERROR: Could not open file {}".format(file_path))
		exit(1)

	size = (WIDTH, HEIGHT)
	main_image.thumbnail(size, Image.ANTIALIAS)

	#traverse through the word matrix
	for i in range(13):
		for j in range(10):
			left= j*WIDTH/10
			right= (j+1)*WIDTH/10
			try:
				top= 126+(HEIGHT-126)/13.8*i
			except ZeroDivisionError:
				top= 126+0
			bottom= 126+(HEIGHT-126)/13.8*(i+1)

			pil_image = main_image.crop((left,top,right,bottom))

			opencv_img= pil_to_opencv(pil_image)
			dominant_color= unique_count(opencv_img)
			if dominant_color[0]>dominant_color[2]: blue.append((i,j))
			if dominant_color[0]<dominant_color[2]: orange.append((i,j))

			thresh= simple_threshold(opencv_img)

			#check which is more(b or w?)
			count= Counter(thresh.flatten())
			if count[0]>count[255]:
				thresh= cv2.bitwise_not(thresh)

			pil_image= opencv_to_pil(thresh)
			pil_image= pil_image.crop((6,8,25,24))
			opencv_img= pil_to_opencv(pil_image)

			img_arr.append(reshape_img(opencv_img))
	
	prediction= np.array(svm_model.predict(img_arr))
	prediction= np.reshape(prediction,(13,10))

	grid= np.vectorize(lambda x: alph_dict[x])(prediction)
	return grid, blue, orange

def pil_to_opencv(pil_image):
	opencv_image = np.array(pil_image) 
	opencv_image = opencv_image[:, :, ::-1].copy()
	return opencv_image

def opencv_to_pil(opencv_im):
	opencv_im = cv2.cvtColor(opencv_im,cv2.COLOR_BGR2RGB)
	pil_im = Image.fromarray(opencv_im)
	return pil_im

def simple_threshold(opencv_image):
	gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
	return thresh

if __name__=="__main__":
	test_img= cv2.imread("train_images/img_118.png")
	pred= svm_model.predict([reshape_img(test_img)])
	print(alph_dict[pred[0]])

	grid, blue, orange= get_grid("test.png")
