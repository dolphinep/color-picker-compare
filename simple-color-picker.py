import cv2
import numpy as np
import math
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

def ColorPicker(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN :  # checks mouse moves    
        colorsBGR = image[y, x]
        colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
        print("RGB Value at ({},{}):{} ".format(x,y,colorsRGB))

        '''show XYZ andLAB'''
        rgb = sRGBColor(colorsRGB[0]/255, colorsRGB[1]/255, colorsRGB[2]/255)
        xyz = convert_color(rgb, XYZColor, target_illuminant='d65')
        LabPic = convert_color(xyz, LabColor)
        print("XYZ value is ", xyz)
        print("LAB value is ", LabPic)

        '''print delta_e for all tester_colors'''
        min_delta_e = Delta_E(LabPic)
        print("Min delta e is color", min_delta_e)
        print("Color : ", tester_colors.index(min_delta_e)+1)

        '''find closet color from RGB different
        closet = GetClosetColorFromTester(colorsRGB)
        print("Closet color(RGB dif) is ", closet+1)'''


        '''draw circle for select color'''      
        colorsFormat = (int(colorsRGB[2]),int(colorsRGB[1]),int(colorsRGB[0])) #color in circle use GRB
        cv2.circle(image, (50,50),50,colorsFormat, -1, 8,0)
        
        '''draw circle for tester color''' 
        resultFormat = (int(min_delta_e[2]),int(min_delta_e[1]),int(min_delta_e[0]))
        cv2.circle(image, (150,50),50,resultFormat, -1, 8,0)


def Chart(event, x, y, flags, param):
    global click
    if event == cv2.EVENT_LBUTTONDOWN :  # checks mouse moves
        colorsBGR = image2[y, x]
        colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
        print("RGB Value at image2 is ({},{}):{} ".format(x,y,colorsRGB))
        tester_colors[click%8] = colorsRGB
    if event == cv2.EVENT_RBUTTONDOWN :
        click = click + 1

'''print delta E value'''
def Delta_E(LabPic):
    color = (0,0,0)
    min_delta_e = 99999
    for rgbColor in tester_colors:
        sRGB = sRGBColor(rgbColor[0]/255,rgbColor[1]/255,rgbColor[2]/255)  #s = small rgb by divided 255
        xyz = convert_color(sRGB, XYZColor, target_illuminant='d65')
        LabTester = convert_color(xyz, LabColor)
        delta_e = delta_e_cie1976(LabPic, LabTester)
        #print("delta_e of color",rgbColor,"is", delta_e)
        if delta_e < min_delta_e:
            min_delta_e = delta_e
            color = rgbColor
    return color
    
''' Color distance Difference of rgb'''
def ColorDistance(rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = 0.5*(rgb1[0]+rgb2[0])
    dif_r = rgb1[0]-rgb2[0]
    dif_g = rgb1[1]-rgb2[1]
    dif_b = rgb1[2]-rgb2[2]
    d = ( ((2+rm/256)*dif_r**2) + (dif_g**2)+((3-rm/256)*dif_b**2))**0.5
    return d

''' Closet color '''
def GetClosetColorFromTester(rgb):
   distance = 999999
   out = -1
   for i in range(len(tester_colors)):
      new_distance = ColorDistance(rgb,tester_colors[i])
      if new_distance < distance:
         distance = new_distance
         out = i
   return out

def palette(colors):
   x=0
   for rgbColor in colors:
      bgrColor = (int(rgbColor[2]),int(rgbColor[1]),int(rgbColor[0]))
      cv2.rectangle(tester_image, (x,0), (x+100,100), bgrColor, -1)
      x+=100

# Tester Color 
tester_colors = [
   (255,255,255),
   (255,255,255),
   (255,255,255),
   (255,255,255),
   (255,255,255),
   (255,255,255),
   (255,255,255),
   (255,255,255)
   ]

# Read an image
image = cv2.imread("human.jpg", cv2.IMREAD_COLOR)
tester_image = 255 * np.ones(shape=[100, 800, 3], dtype=np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX 


# Create a window and set Mousecallback to a function for that window
cv2.namedWindow('ColorPicker')
cv2.setMouseCallback('ColorPicker', ColorPicker)

# Read second image
image2 = cv2.imread("chart.jpg", cv2.IMREAD_COLOR)
cv2.namedWindow('Chart')
cv2.setMouseCallback('Chart', Chart)
click = 0
# Do until esc pressed
while (1):
    
    palette(tester_colors)
    cv2.putText(image,'Select ',(0,150),font,0.5,(255,255,255),2)
    cv2.imshow("Tester",tester_image)
    cv2.imshow('ColorPicker', image)
    cv2.imshow('Chart', image2)
    if cv2.waitKey(10) & 0xFF == 27:
        break
 
# if esc is pressed, close all windows.
cv2.destroyAllWindows()
