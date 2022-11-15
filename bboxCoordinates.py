import cv2
import os
from imageHandle import readImage, printImage,coordinatesAfterResize
from xml.dom import minidom

def readXmlFile(distance):
    objs = []
    file = minidom.parse(os.path.join('data','xmlFiles',distance+'.xml'))
    objects = file.getElementsByTagName('object')
    for index,object in enumerate(objects):
        name = object.getElementsByTagName('name')[0].firstChild.data
        xmin = int(object.getElementsByTagName('bndbox')[0].getElementsByTagName('xmin')[0].firstChild.data)
        xmax = int(object.getElementsByTagName('bndbox')[0].getElementsByTagName('xmax')[0].firstChild.data)
        ymin = int(object.getElementsByTagName('bndbox')[0].getElementsByTagName('ymin')[0].firstChild.data)
        ymax = int(object.getElementsByTagName('bndbox')[0].getElementsByTagName('ymax')[0].firstChild.data)
        objs.append([name,xmin,ymin,xmax,ymax])
    return objs

