import cv2
import numpy as np
import keyboard


def nothing(x):
    pass

cv2.namedWindow('sliders')
img = np.zeros((100,500), np.uint8)

cv2.createTrackbar('Vmin','sliders',62,255,nothing)
cv2.createTrackbar('Vmax','sliders',255,255,nothing)
cv2.createTrackbar('Smin','sliders',42,255,nothing)
cv2.createTrackbar('Smax','sliders',160,255,nothing)
cv2.createTrackbar('Hmin','sliders',38,255,nothing)
cv2.createTrackbar('Hmax','sliders',81,255,nothing)
cv2.createTrackbar('MovementMin', 'sliders', 8, 30,nothing)
cv2.createTrackbar('MovementMax', 'sliders', 14, 30,nothing)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

izqPressed = False
derPressed = False
arrPressed = False
abjPressed = False
state = 0
counter = 0

captura = cv2.VideoCapture(0) 
while(True):
    disponible, fotograma = captura.read()
        
    if (disponible == True):
        
        if(state == 0):
            height = fotograma.shape[0]
            width = fotograma.shape[1]
            thirdW = round(width/3)
            thirdH = round(height/3)
            gray1 = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
            gray2 = gray1.copy()
            state = 1
            ratio = 100.0/(width*height)
        elif(state == 1):
            gray2 = gray1.copy()
            gray1 = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
            movement = cv2.absdiff(gray2,gray1)
             ret, thresh = cv2.threshold(movement,30, 255, cv2.THRESH_BINARY)
            area = cv2.countNonZero(thresh)*ratio
            mMin = cv2.getTrackbarPos('MovementMin','sliders')
            mMax = cv2.getTrackbarPos('MovementMax','sliders')
            
            if(area>= mMin and area <= mMax):
                keyboard.press_and_release('space')
                
                   
        fotograma =  cv2.flip(fotograma, 1)
        fotograma = cv2.blur(fotograma,(5,5))
        
        hsv = cv2.cvtColor(fotograma, cv2.COLOR_BGR2HSV)
        hMin = cv2.getTrackbarPos('Hmin','sliders')
        sMin = cv2.getTrackbarPos('Smin','sliders')
        vMin = cv2.getTrackbarPos('Vmin','sliders')
        
        hMax = cv2.getTrackbarPos('Hmax','sliders')
        sMax = cv2.getTrackbarPos('Smax','sliders')
        vMax = cv2.getTrackbarPos('Vmax','sliders')
        
        HSVmin = (hMin, sMin, vMin)
        HSVmax = (hMax, sMax, vMax)
        
        imgSegmentada = cv2.inRange(hsv,HSVmin,HSVmax)
        imgSegmentada = cv2.morphologyEx(imgSegmentada, cv2.MORPH_OPEN, kernel)
        
        gray = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
        gray = cv2.multiply(gray,0.5)
        grayRGB = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
        fondo = cv2.bitwise_and(grayRGB,grayRGB, mask = 255-imgSegmentada)
        frente = cv2.bitwise_and(fotograma,fotograma, mask = imgSegmentada)
        salida = cv2.add(fondo,frente)
        
        M = cv2.moments(imgSegmentada)
        
        if(M['m00'] > 1000):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            salida = cv2.circle(salida,(cx,cy),5,(0,255,0))
            
            izqPressed = False
            derPressed = False
            arrPressed = False
            abjPressed = False
            if(0 < cx < thirdW):
                izqPressed = True
            elif((thirdW*2 < cx < width)):
                derPressed = True
            if(0 < cy < thirdH):
                arrPressed = True
            elif((thirdH*2 < cy < height)):
                abjPressed = True
            
            if(izqPressed):
                keyboard.press("left")
            else:
                keyboard.release("left")
            if(derPressed):
                keyboard.press("right")
            else:
                keyboard.release("right")
            if(arrPressed):
                keyboard.press("up")
            else:
                keyboard.release("up")
            if(abjPressed):
                keyboard.press("down")
            else:
                keyboard.release("down")
        else:
            if(izqPressed):
                izqPressed = False
                keyboard.release("left")
            if(derPressed):
                derPressed = False
                keyboard.release("right")
            if(arrPressed):
                arrPressed = False
                keyboard.release("up")
            if(abjPressed):
                abjPressed = False
                keyboard.release("down")
        salida = cv2.line(salida,(thirdW,0),(thirdW,height),(255,255,0))
        salida = cv2.line(salida,(thirdW*2,0),(thirdW*2,height),(255,255,0))
        salida = cv2.line(salida,(0,thirdH),(width,thirdH),(255,255,0))
        salida = cv2.line(salida,(0,thirdH*2),(width,thirdH*2),(255,255,0))
        cv2.imshow('salida',salida)
        
    
    else:
        print("Cámara no disponible")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
captura.release()
cv2.destroyAllWindows() 