import numpy as np
import tkinter as tk
import cv2
from skimage.color import rgb2gray
from skimage.io import imread
from skimage import feature
from skimage.morphology import binary_dilation, binary_erosion
import matplotlib.pyplot as plt
import labelshare
import HomeGUI
# from HomeGUI import ImagePage
import sys
import skimage.filters as filters

# Imports image from yolo phone detection
#from yolo_object_detection import img
img_path = sys.argv[1]
#img4 = cv2.imread(img_path)
img4 = cv2.imread("C:/Users/Owner/Documents/11.png")


#Processes image to greyscale
def preprocess(img4):
    #image1 = imread(img)
    image1 = rgb2gray(img4)
    img_edge = binary_erosion(binary_dilation(feature.canny(image1, sigma=.1)))
    return img4, img_edge


fig = plt.figure(figsize=(8, 6))

img1, c1 = preprocess(img4)

ax1 = fig.add_subplot(121)
plt.imshow(img1, cmap='gray')
ax2 = fig.add_subplot(122)
plt.imshow(c1, cmap='gray')

plt.show()

# Result should be in binary (1 for a crack, 0 for no crack)
def edge_prob(window, cut_off):
    pixels = np.array(window.ravel())
    if ((np.count_nonzero(pixels) / len(pixels)) > cut_off):
        return 1
    else:
        return 0

#Forms a 10x10 scanner that slides over the image that returns 1 or 0 depending if cracks are found
# cut_off is the threshold for defining a crack is present or not. (Can be scaled 0-1)
def sliding_mat(img4, window_x=10, window_y=10, cut_off=.0000000000000000000001):
    arr_x = np.arange(0, img4.shape[0], window_x)
    arr_y = np.arange(0, img4.shape[1], window_y)

    canny_edge = np.zeros((len(arr_x), len(arr_y)))

# Begins scanning
    for i, x in enumerate(arr_x):
        for j, y in enumerate(arr_y):
            window = img1[x:x + window_x, y:y + window_y]
            #A[i,j] is a binary matrix taken from the scanner
            canny_edge[i, j] = edge_prob(window, cut_off=cut_off)

    return canny_edge, arr_x, arr_y

# Plots origional image, edge detected image, and masked image
def plot_all(img4, canny_edge, A):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(131)
    ax1.imshow(img4, cmap="gray")
    ax1.set_title("Original")

    ax2 = fig.add_subplot(132)
    ax2.set_title("Canny Edge Detection")
    ax2.imshow(canny_edge, cmap="gray")

    ax3 = fig.add_subplot(133)
    ax3.set_title("Mask")
    ax3.imshow(canny_edge, cmap="gray")
    plt.show()


canny_edge, arr_x, arr_y = sliding_mat(c1, window_x=10, window_y=10, cut_off=.0000000000000000000001)

#prints the amount of phone screen that is cracked to 2 decimal places
print(canny_edge.size,canny_edge)
print("Estimate of crack : {:.2f}%".format(np.sum(canny_edge) / canny_edge.size * 100))

#edges = feature.canny(canny_edge)

# Threshold the edge detection output to create a binary image
#binary_image = np.where(edges > 0, 1, 0)
#print(binary_image)
# Apply thresholding
# Canny edge detection without blur

# Resize image
width, height = 408, 774
img4 = cv2.resize(img4, (width, height))
canny_edge = cv2.Canny(img4, 15, 25, L2gradient=True)

# Threshold the edge map to get a binary matrix
thresh_value = 0.5  # adjust this threshold value between 0 and 1
_, binary_image = cv2.threshold(canny_edge.astype(np.float32), thresh_value, 1, cv2.THRESH_BINARY)

np.savetxt('binary_image.txt', binary_image, fmt='%d')
total_pixels = binary_image.shape[0] * binary_image.shape[1]
white_pixels = np.count_nonzero(binary_image)
edge_percentage = white_pixels / total_pixels * 100

print("Percentage of edges detected:", edge_percentage,white_pixels,total_pixels)


quality1 = ""

if edge_percentage <= 1.35:
    print("PHONE IS LIKE NEW")
    quality1 = "Like New"
elif edge_percentage > 1.35  and edge_percentage <= 1.75 :
    print("PHONE IS EXCELLENT QUALITY")
    quality1 = "Excellent"
elif edge_percentage > 1.75  and edge_percentage <= 2.15 :
    print("PHONE IS GOOD QUALITY")
    quality1 = "Good"
elif edge_percentage > 2.15  and edge_percentage <=3.33 :
    print("PHONE IS OK QUALITY")
    quality1 = "Ok Quality"
else:
    print("PHONE IS POOR QUALITY")
    quality1 = "Poor"





cv2.imshow("CE",canny_edge)


#plot_all(img1, c1, canny_edge)

#
# # Convert the image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Apply Canny edge detection
# edges = cv2.Canny(img, 100, 200)
#
# # Count the number of edge pixels and calculate the percentage of edge pixels
# num_edge_pixels = np.sum(edges)
# total_pixels = edges.shape[0] * edges.shape[1]
# percentage = num_edge_pixels / total_pixels * 100
#
# # Print the result
# print(num_edge_pixels,total_pixels,"Percentage of edge pixels: {:.2f}%".format(percentage))