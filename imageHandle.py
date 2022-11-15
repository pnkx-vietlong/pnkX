import numpy as np
import cv2
import os

def readImage(file):
    img = cv2.imread(file)
    return img

def resizeImage(img,img_size):
    img = cv2.resize(img,(img_size,img_size))
    return img

def writeImage(img,path):
    files = list(filter(lambda f: f.endswith('.jpg') and not (f.startswith('Original Image') or f.startswith('Resized Image')),os.listdir(path)))
    files.sort()
    print(files)
    if len(files) == 0:
        cv2.imwrite(os.path.join(path,'0.jpg'),img)
    else:
        last_file = files[-1]
        number = int(last_file[:-4])
        cv2.imwrite(os.path.join(path,str(number+1)+'.jpg'),img)

def printImage(img,bboxes):
    print('Coordinates to print:',bboxes)
    for i in range(len(bboxes)):
        cv2.rectangle(img,((bboxes[i][1]),bboxes[i][2]),(bboxes[i][3],bboxes[i][4]),(255,0,0),1)
        cv2.putText(img,bboxes[i][0],(bboxes[i][1],bboxes[i][2]-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,0),2)
    cv2.imshow('window',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def coordinatesAfterResize(img,bboxes,size):
    new_coordinates = []
    x_scale = size/img.shape[1]
    y_scale = size/img.shape[0]
    for i in range(len(bboxes)):
        # print(bboxes[i][1:])
        xmin,ymin,xmax,ymax = bboxes[i][1:]
        new_xmin = int(np.round(xmin*x_scale))
        new_ymin = int(np.round(ymin*y_scale))
        new_xmax= int(np.round(xmax*(x_scale)))
        new_ymax= int(np.round(ymax*y_scale))
        bboxes[i][1:] = [new_xmin,new_ymin,new_xmax,new_ymax]
    return bboxes
