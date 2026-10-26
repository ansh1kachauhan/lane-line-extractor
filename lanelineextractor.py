import cv2
import os
import numpy

    
road1= cv2.imread(r"C:\Users\c31an\Desktop\laneliner\images\road1.jpe")
img= cv2.imread(r"C:\Users\c31an\Desktop\laneliner\images\road1.jpe")
img2=cv2.imread(r"C:\Users\c31an\Desktop\laneliner\images\road2.jpe")
print(type(img)) #image is an array of numbers
print(img.shape) #height and width of image
print(img[0,0]) #colour of top left pixel in bgr format

img[100:150,300:350]=(0,0,255) #changing the colour of a portion
cv2.imwrite("result.jpg", img) # saving the result


gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray.shape) #no third dimension

hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #hsv 

whitemask=cv2.inRange(hsv, (0,0,200), (179,40,255)) #masking
yellowmask=cv2.inRange(hsv, (15,80,100), (35,255,255))
mask=cv2.bitwise_or(whitemask, yellowmask)

cv2.imwrite("mask.jpg",mask)

hsv2=cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
whitemask2=cv2.inRange(hsv2, (0,0,200), (179,40,255))
yellowmask2=cv2.inRange(hsv2, (15,80,100), (35,255,255))

mask2=cv2.bitwise_or(whitemask2, yellowmask2)
cv2.imwrite("mask2.jpg",mask2)

blur=cv2.GaussianBlur(road1, (15,15),3) #blurring
cv2.imwrite("blur.jpg", blur)

edge=cv2.Canny(blur, 50,150) #edge detection
cv2.imwrite("edge.jpg",edge)



h,w= edge.shape
roimask=numpy.zeros_like(edge)

trapezoid=numpy.array([[ (0,h), # bottom-left
                        (w, h), # bottom-right
    (int(0.55 * w), int(0.6 * h)),  # top-right
    (int(0.45 * w), int(0.6 * h)),  # top-left
]])

cv2.fillPoly(roimask, trapezoid, 255)
roiresult=cv2.bitwise_or(edge,roimask)
cv2.imwrite("roiresult.jpg", roiresult)

debug=road1.copy()
cv2.polylines(debug,trapezoid,True,(0,255,0),3)
cv2.imwrite("debug.jpg",debug)



