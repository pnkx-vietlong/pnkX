import os

#exp gần nhất
def pwd(distance):
    folders = [int(i[3:]) for i in os.listdir(os.path.join('data','images',distance))]
    folders.sort()
    last_folder = folders[-1]
    return os.path.join('data','images',distance,'exp'+str(last_folder))

#file ảnh cuối của exp gần nhất
def lastestFile(distance):
    lastestExp = pwd(distance)
    files = list(filter(lambda f: f.endswith('.jpg') and not (f.startswith('Original Image') or f.startswith('Resized Image')),os.listdir(lastestExp)))
    numbers = [int(i[:-4]) for i in files]
    numbers.sort()
    lastFile = str(numbers[-1])+'.jpg'
    return os.path.join(lastestExp,lastFile)

#tạo exp mới
def mkdir(distance):
    dir = os.path.join('data','images',distance)
    numbers = [int(i[3:]) for i in os.listdir(dir)]
    if len(numbers)==0:
        os.makedirs(os.path.join(dir,'exp1'))
        numbers.append('exp1')
    else:
        numbers.sort()
        number = numbers[-1]
        print('number',number)
        os.makedirs(os.path.join(dir,'exp'+str(number+1)))
        numbers.append('exp'+str(number+1))
    path = os.path.join(dir,numbers[-1])        
    return path       

def writeTxtFile1(path,shape,bboxes):
    f = open(os.path.join(path,'infor.txt'),'a+')
    f.write('Input Shape: '+str(shape[0])+'x'+str(shape[1])+'\n')
    f.write('Coordinates:\n')
    for box in bboxes:
        f.write('\t'+box[0]+': '+str(box[1])+' '+str(box[2])+' '+str(box[3])+' '+str(box[4])+'\t=> Shape: '+'('+str(box[3]-box[1])+'x'+str(box[4]-box[2])+')\n')
    f.write('\n')
    f.close()

def writeTxtFile2(path,shape,bboxes,size):
    f = open(os.path.join(path,'infor.txt'),'a+')
    f.write('Resize to '+str(size))
    f.write('Output Shape: '+str(shape[0])+'x'+str(shape[1])+'\n')
    f.write('Coordinates:\n')
    for box in bboxes:
        f.write('\t'+box[0]+': '+str(box[1])+' '+str(box[2])+' '+str(box[3])+' '+str(box[4])+'\t=> Shape: '+'('+str(box[3]-box[1])+'x'+str(box[4]-box[2])+')\n')
    f.write('\n')
    f.close()

def writeTxtFile3(path,kernel_size,stride,padding,shape,bboxes,file):
    f = open(os.path.join(path,'infor.txt'),'a+')
    f.write('Conv('+str(kernel_size)+','+str(stride)+','+str(padding)+')\n') 
    f.write('Output Size: '+str(shape[0])+'x'+str(shape[1])+'\n')
    f.write('Coordinates:\n')
    for box in bboxes:
        f.write('\t'+box[0]+': '+str(box[1])+' '+str(box[2])+' '+str(box[3])+' '+str(box[4])+'\t=> Shape: '+'('+str(box[3]-box[1])+'x'+str(box[4]-box[2])+')\n')
    f.write('Save image at: '+os.path.join(path,file)+'\n')
    f.write('\n')
    f.close()