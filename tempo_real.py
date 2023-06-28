import numpy as np
import cv2

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    # Lê o próximo quadro de vídeo
    ret, frame = cap.read()

    # Converte o quadro de vídeo para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define os valores mínimos e máximos da cor vermelha em HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

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
    width_black = 196  # Largura da área preta em mm
    height_black = 160  # Altura da área preta em mm

    # Variáveis para armazenar as coordenadas do centro e do topo direito da área preta
    center_x = 0
    center_y = 0
    top_right_x = 0
    top_right_y = 0

    # Encontra a menor área preta em relação à área vermelha
    min_area = float('inf')
    min_contour = None

    for cnt_black in contours_black:
        x_black, y_black, w_black, h_black = cv2.boundingRect(cnt_black)

        if w_black <= width_black and h_black <= height_black:
            for cnt_red in contours_red:
                x_red, y_red, w_red, h_red = cv2.boundingRect(cnt_red)

                # Calcula as dimensões da área preta em relação à área vermelha
                x_relative = x_red - x_black  # Posição X relativa da área vermelha em relação à área preta
                y_relative = y_red - y_black  # Posição Y relativa da área vermelha em relação à área preta
                w_relative = w_red  # Largura da área vermelha em relação à área preta (mesma largura)
                h_relative = h_red  # Altura da área vermelha em relação à área preta (mesma altura)

                # Calcula a área da área preta em relação à área vermelha
                area_ratio = (w_relative * h_relative) / (w_black * h_black)

                # Verifica se a área é a menor encontrada até agora
                if area_ratio < min_area:
                    min_area = area_ratio
                    min_contour = cnt_red
                    center_x = int(x_black + w_black / 2)  # Coordenada X do centro relativa à área preta
                    center_y = int(y_black + h_black / 2)  # Coordenada Y do centro relativa à área preta
                    top_right_x = x_black + w_black  # Coordenada X do topo direito relativa à área preta
                    top_right_y = y_black  # Coordenada Y do topo direito relativa à área preta

    # Conversão das coordenadas do centro para centímetros
    center_x_mm = (center_x / frame.shape[1]) * width_black
    center_y_mm = (center_y / frame.shape[0]) * height_black

    # Desenha um retângulo em volta da área preta
    for cnt_black in contours_black:
        x_black, y_black, w_black, h_black = cv2.boundingRect(cnt_black)
        cv2.rectangle(frame, (x_black, y_black), (x_black + w_black, y_black + h_black), (0, 0, 0), 2)

    # Desenha um retângulo em volta da menor área vermelha em relação à área preta
    if min_contour is not None:
        x_red, y_red, w_red, h_red = cv2.boundingRect(min_contour)
        cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2)
        # Exibe as coordenadas do centro da menor área vermelha em centímetros
        print("Coordenadas do centro da menor área vermelha:")
        print(f"{center_x_mm}, {center_y_mm}")

    # Mostra a imagem original com a área preta e a menor área vermelha encontradas destacadas
    cv2.imshow('Camera', frame)

    # Verifica se a tecla 'q' foi pressionada para encerrar o loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura da câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()

