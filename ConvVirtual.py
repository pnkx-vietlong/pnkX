import numpy as np
import cv2
import os
import argparse

def readImage(img_path):
    img = cv2.imread(img_path)
    return img

def resizeImage(img,img_size):
    img = cv2.resize(img,(img_size,img_size))
    return img

def writeImage(img,path):
    files = list(filter(lambda f: f.endswith('.jpg'),os.listdir(path)))
    files.sort()
    if len(files) == 0:
        cv2.imwrite(os.path.join(path,'0.jpg'),img)
    else:
        last_file = files[-1]
        number = int(last_file[:-4])
        cv2.imwrite(os.path.join(path,str(number+1)+'.jpg'),img)

#exp gần nhất
def pwd(distance):
    folders = os.listdir(os.path.join('images',distance))
    folders.sort()
    last_folder = folders[-1]
    return os.path.join('images',distance,last_folder)

#file ảnh cuối của exp gần nhất
def lastestFile(distance):
    lastestExp = pwd(distance)
    files = list(filter(lambda f: f.endswith('.jpg'),os.listdir(lastestExp)))
    files.sort()
    lastFile = files[-1]
    return os.path.join(lastestExp,lastFile)

#tạo exp mới
def mkdir(distance):
    dir = os.path.join('images',distance)
    folder = os.listdir(dir)
    if len(folder)==0:
        os.makedirs(os.path.join(dir,'exp1'))
        folder.append('exp1')
    else:
        folder.sort()
        last_folder = folder[-1]
        number = int(last_folder[-1])
        os.makedirs(os.path.join(dir,'exp'+str(number+1)))
        folder.append('exp'+str(number+1))
    path = os.path.join(dir,folder[-1])        
    return path       

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
    def write(self,path,fileName):
        cv2.imwrite(os.path.join(path,(fileName+'.jpg')),self.output)

# class PoolVirtual:
#     def __inti__(self,)
# 20m
def action(distance,size):
    img = readImage(os.path.join('images',distance+'.jpg'))
    img = resizeImage(img,size)
    savingDir = mkdir(distance)
    f = open(os.path.join(savingDir,'infor.txt'),mode = 'a+')
    f.write('Input Size: '+str(size)+'x'+str(size)+'\n')
    
    conv = ConvVirtual(3,2,0,img)
    img = conv.forward()

    f.write('Conv('+str(conv.kernel_size)+','+str(conv.stride)+','+str(conv.padding)+') => Output Size:'+str(img.shape[0])+'x'+str(img.shape[1])+'\n')
    writeImage(img,savingDir)
    for i in range(3):
        lastFile = lastestFile(distance)
        print('lastfile: ',lastFile)
        img = readImage(lastFile)
        savingDir = pwd(distance)

        conv = ConvVirtual(3,2,0,img)
        img = conv.forward()

        f.write('Conv('+str(conv.kernel_size)+','+str(conv.stride)+','+str(conv.padding)+') => Output Size:'+str(img.shape[0])+'x'+str(img.shape[1])+'\n')
        writeImage(img,savingDir)
    
    f.close()


action('80m',1280)
# img = resizeImage(img,416)

# savingDir = pwd('20m')

# conv = ConvVirtual(3,2,0,img)
# img = conv.forward()
# writeImage(img,savingDir)
# conv.forward()
# conv.write()