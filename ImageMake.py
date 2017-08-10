import numpy as np    
from math import *    
import sys    
import os    
import glob    
import argparse    
import cv2 as cv   
import keras
import random
from matplotlib import pyplot as plt
def onmouse(event, x, y, flags, param):#鼠标事件响应函数    
    global drag_start, sel, lab, sets, count 
    if event == cv.EVENT_LBUTTONDOWN:#左键按下时记录当前初始坐标，并初始化矩形sel    
        drag_start = x, y    
        sel = 0,0,0,0   
        sam=0,0,0,0   
        if count==100:
            lab+=1
        if count==200:
            lab+=1
        if count>=300:
            print('over all')
        count+=1
    elif event == cv.EVENT_LBUTTONUP:#鼠标左键叹弹起时响应    
        if sel[2] > sel[0] and sel[3] > sel[1]:#判断右下角坐标是否大于左上角   
            mid=int((sel[1]+sel[3])/2),int((sel[0]+sel[2])/2)
            sam=mid[0]-14,mid[1]-14,mid[0]+14,mid[1]+14
            patch = gray[sam[0]:sam[2],sam[1]:sam[3]]#取矩形区域内像素作为patch图像  
            target = cv.cvtColor(patch, cv.COLOR_GRAY2BGR)#取矩形区域内原始像素截取图像 
            #sets.append([target,int(input('lab:'))])
            sets.append([target,lab])
            print(target.shape,sam,count,lab,sam[0],sam[1],sam[2],sam[3])
            np.save('cloud',sets)
            #plt.imsave('sample.jpg',target)
        drag_start = None    
    elif drag_start:    
        #print flags    
        if flags & cv.EVENT_FLAG_LBUTTON:#取当前坐标与初始坐标较小的为矩形坐标左上，较大的为右下    
            minpos = min(drag_start[0], x), min(drag_start[1], y)    
            maxpos = max(drag_start[0], x), max(drag_start[1], y)    
            sel = minpos[0], minpos[1], maxpos[0], maxpos[1]    
            img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)    
            cv.rectangle(img, (sel[0], sel[1]), (sel[2], sel[3]), (0,255,255), 1)    
            #print(sel[0],sel[1],sel[2],sel[3])
            cv.imshow("gray", img)    
        else:    
            print ("selection is complete" )
            drag_start = None    

drag_start = None#全局变量取方块鼠标拖拽时使用    
sel = (0,0,0,0)#全局变量 长方形左上颌右下定点坐标存储    
lab=0
sets=[]  
count=0
#filename = 'HC421.jpg'   
filename = 'up.jpg'   
cv.namedWindow("gray",1) # 第二个参数　１窗口固定；２窗口可调整   
cv.setMouseCallback("gray", onmouse)     
 
ext = os.path.splitext(filename)[1][1:] #get the filename extenstion    
if ext == "png" or ext == "jpg" or ext == "bmp" or ext == "tiff" or ext == "pbm":    
    print (filename )   
                
    img=cv.imread(filename,1)    
    sel = (0,0,0,0)    
    drag_start = None    
    gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)    
    cv.imshow("gray",gray)    
    cv.waitKey(0)
 
cv.destroyAllWindows()   