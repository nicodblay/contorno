import cv2
import numpy as np
from matplotlib import pyplot as plt


#cargar la imagen a analizar
imagen= cv2.imread("tomate22.jpg")
#cv2.imshow("Original", imagen)
#cv2.waitKey(0)

# Convertimos en escala de grise
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#cv2.imshow("En gris", gris)
#cv2.waitKey(0)

# Aplicar suavizado Gaussiano
gaussiana = cv2.GaussianBlur(gris, (5,5), 0)
#cv2.imshow("Gaussiano", gaussiana)
#cv2.waitKey(0)

#detectamos los bordes con canny
sigma=0.9
v=np.median(gaussiana)
lower=int(max(0,(1.0-sigma)*v))
upper=int(min(255,(1.0+sigma)*v))
canny = cv2.Canny(gaussiana, lower, upper)
#cv2.imshow("Canny", canny)
#cv2.waitKey(0)

x=5
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x,x))
dilation = cv2.dilate(canny,kernel,iterations = 1)
cv2.imshow("Dilatado", dilation)
cv2.waitKey(0)

#buscamos los contornos
(_,contornos,_) = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imagen,contornos,-1,(255,0,0), 2)
cv2.imshow("contornos", imagen)
cv2.waitKey(0)

cv2.destroyAllWindows()