import cv2
import numpy as np

# Captura o vídeo da câmera
cap = cv2.VideoCapture(0)

# Aguarda o usuário pressionar a tecla 's'
while True:
    ret, frame = cap.read()
    cv2.imshow('Pressione "s" para iniciar', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

while True:
    # Lê o frame do vídeo
    ret, frame = cap.read()

    if not ret:
        break

    # Converte o frame de BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define os valores mínimos e máximos da cor vermelha em HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([160,100,100])
    upper_red2 = np.array([179,255,255])

    # Cria uma máscara para a cor vermelha
    mask_red1 = cv2.inRange(hsv, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Define os valores mínimos e máximos da cor preta em HSV
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 30])

    # Cria uma máscara para a cor preta
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # Encontra os contornos da área preta
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontra os contornos da área vermelha
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variáveis para armazenar as dimensões da área preta
    width_black = 100  # Largura da área preta em mm
    height_black = 100  # Altura da área preta em mm

    # Variáveis para armazenar as coordenadas do centro da maior área vermelha
    center_x = 0
    center_y = 0

    # Encontra a maior área vermelha em relação à área preta
    max_area = -1
    max_contour = None

    for cnt_black in contours_black:
        x_black, y_black, w_black, h_black = cv2.boundingRect(cnt_black)

        if w_black >= width_black and h_black >= height_black:
            for cnt_red in contours_red:
                x_red, y_red, w_red, h_red = cv2.boundingRect(cnt_red)

                # Calcula as dimensões da área vermelha em relação à área preta
                x_relative = x_red - x_black  # Posição X relativa da área vermelha em relação à área preta
                y_relative = y_red - y_black  # Posição Y relativa da área vermelha em relação à área preta
                w_relative = w_red  # Largura da área vermelha em relação à área preta (mesma largura)
                h_relative = h_red  # Altura da área vermelha em relação à área preta (mesma altura)

                # Calcula a área da área vermelha em relação à área preta
                area_ratio = (w_relative * h_relative) / (w_black * h_black)

                # Verifica se a área é a maior encontrada até agora
                if area_ratio > max_area:
                    max_area = area_ratio
                    max_contour = cnt_red
                    center_x = int(x_red + w_red / 2)
                    center_y = int(y_red + h_red / 2)

    # Conversão das coordenadas do centro para centímetros
    center_x_mm = (center_x / frame.shape[1]) * width_black
    center_y_mm = (center_y / frame.shape[0]) * height_black

    # Desenha um retângulo em volta da área preta
    for cnt_black in contours_black:
        x_black, y_black, w_black, h_black = cv2.boundingRect(cnt_black)
        cv2.rectangle(frame, (x_black, y_black), (x_black + w_black, y_black + h_black), (0, 0, 0), 2)

    # Desenha um retângulo em volta da maior área vermelha em relação à área preta
    if max_contour is not None:
        x_red, y_red, w_red, h_red = cv2.boundingRect(max_contour)
        cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2)
        # Exibe as coordenadas do centro da maior área vermelha em centímetros
        print("Coordenadas do centro da maior área vermelha:")
        print(f"{center_x_mm}, {center_y_mm}")

    # Mostra a imagem original com a área preta e a maior área vermelha encontradas destacadas
    cv2.imshow('Camera', frame)

    # Verifica se a tecla 'q' foi pressionada para encerrar o loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura da câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
