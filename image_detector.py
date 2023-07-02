import cv2
import imutils
import numpy as np

class ImageDetector():
    def __init__(self,width,height):
        self.width = width
        self.height = height
    
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape
    
    def startDetection(self,image):
        # load the image and resize it to a smaller factor so that the shapes can be approximated better
        resized = imutils.resize(image, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        # convert the resized image to grayscale and blur it slightly
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # apply adaptive thresholding to segment the shapes from the background
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # find contours in the thresholded image and initialize the shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Initialize variables to store the largest rectangle found
        max_area = 0
        max_rect = None

        for c in cnts:
            # compute the center of the contour, then detect the name of the shape using only the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else:
                cX, cY = 0, 0
            shape = self.detect(c)
            shapes = ['square', 'rectangle']
            if shape in shapes:
                # multiply the contour (x, y)-coordinates by the resize ratio
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                
                # compute the area of the contour
                area = cv2.contourArea(c)
                # update the largest rectangle found if necessary
                if area > max_area:
                    max_area = area
                    max_rect = c

        # check if a rectangle was found
        if max_rect is not None:
            # draw the largest rectangle on the image
            cv2.drawContours(image, [max_rect], -1, (0, 255, 0), 2)
            # crop the largest rectangle from the original image
            x, y, w, h = cv2.boundingRect(max_rect)
            crop = image[y:y+h, x:x+w]
            print(crop.shape)

        # show the output image
        if crop is not None:
            return crop
    
    def retrieveCoordinates(self,frame):
        crop = self.startDetection(frame)
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV) 
        # Define os valores mínimos e máximos da cor vermelha em HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # Cria uma máscara para a cor vermelha
        mask_red1 = cv2.inRange(hsv, lower_red, upper_red)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Encontra os contornos da área vermelha
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Variáveis para armazenar as dimensões da maior área preta
        max_area = 0
        max_contour = None

        for countours in contours_red:

            x_red, y_red, w_red, h_red = cv2.boundingRect(countours)
            area = (w_red * h_red)
            print(x_red,y_red)
            #cv2.rectangle(crop, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2)

            # Verifica se a área é a maior encontrada até agora
            if area > max_area:
                max_area = area
                max_contour = countours
                center_x = int(x_red + w_red / 2)  # Coordenada X do centro relativa à área preta
                center_y = int(y_red + h_red / 2)  # Coordenada Y do centro relativa à área preta
                top_left_x = x_red  # Coordenada X do topo esquerdo relativa à área preta
                top_left_y = y_red  # Coordenada Y do topo esquerdo relativa à área preta
                top_height_red = h_red
                top_width_red = w_red
        try:
            cv2.rectangle(crop, (top_left_x, top_left_y), (top_left_x + top_width_red, top_left_y + top_height_red), (0, 0, 255), 2)

            # Conversão das coordenadas do centro para centímetros
            center_x_mm = (center_x / crop.shape[1]) * self.width
            center_y_mm = (center_y / crop.shape[0]) * self.height
            print(center_x,center_y_mm)
            # Desenha um retângulo em volta da maior área vermelha em relação à área preta
            if max_contour is not None:
                x_red, y_red, w_red, h_red = cv2.boundingRect(max_contour)
                
                # Exibe as coordenadas do centro da maior área vermelha em centímetros
                print("Coordenadas do centro da maior área vermelha:")
                print(f"{center_x_mm}, {center_y_mm}")

                # Mostra a imagem original com a área preta e a maior área vermelha encontradas destacadas
            cv2.rectangle(crop, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2)
            return center_x_mm, center_y_mm, crop
        except:
            return -1,-1,crop

