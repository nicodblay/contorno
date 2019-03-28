import cv2
import numpy as np

#cargar la imagen a analizar
imagen= cv2.imread("tomate2.jpg")
cv2.imshow("Original", imagen)
cv2.waitKey(0)

# Convertimos en escala de grise
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
cv2.imshow("En gris", gris)
cv2.waitKey(0)

# Aplicar suavizado Gaussiano
gaussiana = cv2.GaussianBlur(gris, (5,5), 0)
cv2.imshow("Gaussiano", gaussiana)
cv2.waitKey(0)

#detectamos los bordes con canny
canny = cv2.Canny(gaussiana, 50, 150)
cv2.imshow("Canny", canny)
cv2.waitKey(0)

#dilatacion
#kernel = np.ones((5,5),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
dilation = cv2.dilate(canny,kernel,iterations = 1)
cv2.imshow("Dilatado", dilation)
cv2.waitKey(0)

#buscamos los contornos
(_,contornos,_) = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

t=0
valido=np.zeros((10000,3))
novalido=np.zeros((10000,3))
v=0
k=0
for x in range (len(contornos)):
    cv2.drawContours(imagen, [contornos[x]], 0, (t,0,0), 3)
    cv2.imshow("contornos", imagen)
    t=t+20
    print("Es contorno de tomate?")
    c=cv2.waitKey(0) & 0xFF
    if (c==ord("t") ):
        for y in range (0,contornos[x].size,2):
            i=contornos[x].item(y)
            j=contornos[x].item(y+1)
            if (i>=imagen.shape[0] or j>=imagen.shape[1]):
                valido[k]=[0,0,0]   
        
            else:
                azul=imagen.item (i,j,0) #para hallar las intensidad de azul 
                verde=imagen.item (i,j,1) #para hallar las intensidad de verde
                rojo= imagen.item (i,j,2) #para hallar las intensidad de rojo
                valido[k]=[azul,verde,rojo]
        
            k=k+1
        print("Guardado como contorno valido")
        
    if (c==ord("n") ):
        for y in range (0,contornos[x].size,2):
            i=contornos[x].item(y)
            j=contornos[x].item(y+1)
            if (i>=imagen.shape[0] or j>=imagen.shape[1]):
                novalido[k]=[0,0,0]   
        
            else:
                azul=imagen.item (i,j,0) #para hallar las intensidad de azul 
                verde=imagen.item (i,j,1) #para hallar las intensidad de verde
                rojo= imagen.item (i,j,2) #para hallar las intensidad de rojo
                novalido[k]=[azul,verde,rojo]
        
            k=k+1
        print("Guardado como contorno no valido")
        
cv2.destroyAllWindows()


