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
gaussiana = cv2.GaussianBlur(gris, (3,3), 0)
#cv2.imshow("Gaussiano", gaussiana)
#cv2.waitKey(0)

#detectamos los bordes con canny
sigma=0.9
v=np.median(gaussiana)
lower=int(max(0,(1.0-sigma)*v))
upper=int(min(255,(1.0+sigma)*v))
canny = cv2.Canny(gaussiana, lower, upper)
plt.subplot(121),plt.imshow(canny,cmap = 'gray')
plt.title('Canny'), plt.xticks([]), plt.yticks([])
#cv2.imshow("Canny", canny)
#cv2.waitKey(0)

#dilatacion
#kernel = np.ones((5,5),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
dilation = cv2.dilate(canny,kernel,iterations = 1)
#cv2.imshow("Dilatado", dilation)
#cv2.waitKey(0)

#buscamos los contornos
(_,contornos,_) = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imagen,contornos,-1,(255,0,0), 2)
cv2.imshow("contornos", imagen)
cv2.waitKey(0)

for x in range (len(contornos)):
    
    #mascara
    mask=np.zeros_like(imagen)
    out=np.zeros_like(imagen)
    cv2.drawContours(mask, [contornos[x]], 0, (255,0,0), -1) #con ese -1 al final hace que pinte todo de azul lo que esta dentro del borde
    for i in range (imagen.shape[0]): #para recorrer todas las columnas .shape[0]
        for j in range (imagen.shape[1]): #para recorrer todas las filas .shape[1]
            if mask[i,j,0]==255: 
                out[i,j]=imagen[i,j] 
    
    cv2.imshow("contorno", out)
    
    #histograma    
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([out],[i],None,[256],[1,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()

    print("Es contorno de tomate?")
    c=cv2.waitKey(0) & 0xFF
    if (c==ord("t") ):
        
        print("Histograma guardado como valido")
        
    if (c==ord("n") ):

        print("Histograma guardado como no valido")
        
cv2.destroyAllWindows()


