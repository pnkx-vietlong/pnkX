import numpy as np
import cv2
import os
from imageHandle import readImage,resizeImage,writeImage,printImage,coordinatesAfterResize
from fileNfolderHandle import mkdir,lastestFile,pwd,writeTxtFile1,writeTxtFile2,writeTxtFile3
from bboxCoordinates import readXmlFile

class ConvVirtual:
    def __init__(self,kernel_size,stride,padding,image):
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.image = image
    def forward(self):
        self.output = np.full(((self.image.shape[0]-self.kernel_size+2*self.padding)//self.stride+1,
            (self.image.shape[1]-self.kernel_size+2*self.padding)//self.stride+1,
            3),
            124)

        W = int((self.image.shape[1]-self.kernel_size+2*self.padding)//self.stride+1)
        H = int((self.image.shape[0]-self.kernel_size+2*self.padding)//self.stride+1)
        
        if self.padding!=0:
            pad = np.zeros((self.image.shape[0]+2*self.padding,self.image.shape[1]+2*self.padding,3))
            pad[self.padding:self.padding+self.image.shape[0],self.padding:self.padding+self.image.shape[1],:] = self.image[:,:,:]
            self.image = pad
        
        for x in range(H):
            for y in range(W):
                # cv2.imwrite(os.path.join(self.path,'images',str(12*x+y)+'.jpg'),self.image[x*self.stride:x*self.stride+self.kernel_size,y*self.stride:y*self.stride+self.kernel_size])
                self.output[x,y,:] = cv2.resize(self.image[x*self.stride:x*self.stride+self.kernel_size,y*self.stride:y*self.stride+self.kernel_size],(1,1))
        print('Shape after conv:',H,' x',W)
        return self.output

    def coordinates(self,xmin,ymin,xmax,ymax):
        # print(self.kernel_size,self.stride,self.padding)
        new_xmin = int((xmin-self.kernel_size+2*self.padding)//self.stride+1)
        new_ymin = int((ymin-self.kernel_size+2*self.padding)//self.stride+1)
        new_xmax = int((xmax-self.kernel_size+2*self.padding)//self.stride+1)
        new_ymax = int((ymax-self.kernel_size+2*self.padding)//self.stride+1)
        return [new_xmin,new_ymin,new_xmax,new_ymax]
# class PoolVirtual:
#     def __inti__(self,)
# 20m
def action(distance,size):
    # Read Image
    savingDir = mkdir(distance)


    img = readImage(os.path.join('data','images',distance+'.jpg'))

    bboxes = readXmlFile(distance)

    cv2.imwrite(os.path.join(savingDir,'Original Image'+'.jpg'),img)

    writeTxtFile1(savingDir,[img.shape[0],img.shape[1]],bboxes)
    
    # Resize Image
    img = resizeImage(img,size)
    
    bboxes = coordinatesAfterResize(img,bboxes,size)

    cv2.imwrite(os.path.join(savingDir,'Resized Image'+'.jpg'),img)

    writeTxtFile2(savingDir,[img.shape[0],img.shape[1]],bboxes,size)

    # Convolution Layer
    conv = ConvVirtual(3,2,0,img)
    img = conv.forward()

    for i in range(len(bboxes)):
        xmin,ymin,xmax,ymax = bboxes[i][1],bboxes[i][2],bboxes[i][3],bboxes[i][4]
        bboxes[i][1:] = conv.coordinates(xmin,ymin,xmax,ymax)

    writeTxtFile3(savingDir,conv.kernel_size,conv.stride,conv.padding,[img.shape[0],img.shape[1]],bboxes,'0.jpg')
    writeImage(img,savingDir)
    for i in range(3):

        lastFile = lastestFile(distance).split('/')
        img = readImage('/'.join(lastFile))
        conv = ConvVirtual(3,2,0,img)
        img = conv.forward()

        for i in range(len(bboxes)):
            xmin,ymin,xmax,ymax = bboxes[i][1],bboxes[i][2],bboxes[i][3],bboxes[i][4]
            # print(bboxes[i][1:])
            bboxes[i][1:] = conv.coordinates(xmin,ymin,xmax,ymax)
            # print(conv.coordinates(xmin,ymin,xmax,ymax))

        writeTxtFile3(savingDir,conv.kernel_size,conv.stride,conv.padding,[img.shape[0],img.shape[1]],bboxes,str(int(lastFile[-1][:-4])+1)+'.jpg')
        writeImage(img,savingDir)

action('80m',416)
    

# action('80m',1280)


# img = resizeImage(img,416)

# savingDir = pwd('20m')

# conv = ConvVirtual(3,2,0,img)
# img = conv.forward()
# writeImage(img,savingDir)
# conv.forward()
# conv.write()