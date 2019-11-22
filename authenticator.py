import matplotlib.pyplot as plt
import numpy as np
from imutils import contours
from skimage import measure, img_as_ubyte
import argparse
import imutils
import cv2
import face_recognition


from PIL import Image, ImageDraw

class Authenticator:
    
    def __init__(self):
        
        self.known_face_encodings = np.array([])
        self.known_face_id = np.array([])

    def add_user(self, image, id):
        
        if face_recognition.face_encodings(image) == []:
            return False

        if len(self.known_face_encodings) == 0:
            self.known_face_encodings = np.hstack((self.known_face_encodings, face_recognition.face_encodings(image)[0]))
            self.known_face_id = np.hstack((self.known_face_id, id))
    
        else:
            self.known_face_encodings = np.vstack((self.known_face_encodings, face_recognition.face_encodings(image)[0]))
            self.known_face_id = np.hstack((self.known_face_id, id))
    
        return True
    
    def remove_user(self, id):

        ids = np.where(self.known_face_id == id)

        self.known_face_id = np.delete(self.known_face_id, ids)
        
        if len(self.known_face_encodings) == 128:
            self.known_face_encodings = np.array([])
        else:
            self.known_face_encodings = np.delete(self.known_face_encodings, ids, 0)

    def face_crop(self, image):

        def face_area(face):
            top, right, bottom, left = face
            return (bottom-top)*(right-left)
        
        faces_locations = face_recognition.face_locations(image)
        
        # Get the biggest bounding box.
        if faces_locations != []:
            curr_face = faces_locations[0]
            for face in faces_locations:
                if face_area(face) > face_area(curr_face):
                    curr_face = face
        
            return curr_face
        
        return faces_locations

    def face_classifier(self, image):

        face_location = face_recognition.face_locations(image)
        face_encoding = face_recognition.face_encodings(image, face_location)

        if face_encoding == []:
            return ("Face encoding is []", False)

        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
       
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_id[first_match_index]

            return ("User '%s' detected." % (name), True)
        
        return ("User does not exist in database.", False)

    def life_proof(self, RAWimage, debug=0):

        #Ajusta o tamanho da imagem para 800px de largura
        largura = 800
        scale = largura / RAWimage.shape[1]
        if debug:
            print('Escala de resize: ' + str(1/scale))
        
        newdim = (largura, int(RAWimage.shape[0] * scale))
        image = cv2.resize(RAWimage, newdim, interpolation = cv2.INTER_AREA)
        
        if debug:
            cv2.imshow('Processamento Demo', image)
            cv2.waitKey(50)


        # Transforma em preto e branco
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if debug:
            cv2.imshow('Processamento Demo', gray)
            cv2.waitKey(50)


        #equaliza o contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        grayEq = clahe.apply(gray)
        if debug:
            cv2.imshow('Processamento Demo', grayEq)
            cv2.waitKey(50)


        #reconhece os limites da cabeca
        face_locations = face_recognition.face_locations(image)
        #(top, right, bottom, left)
        top = face_locations[0][0]
        right = face_locations[0][1]
        bottom = face_locations[0][2]
        left = face_locations[0][3]


        #Corta a regiao de interesse (crop)
        grayEq = grayEq[top:bottom, left:right]


        #Ajusta o tamanho da ROI para 500px de largura
        largura2 = 500
        scale2 = largura / grayEq.shape[1]
        
        if debug:
            print('Escala de resize 2: ' + str(scale2))
        
        newdim = (largura, int(grayEq.shape[0] * scale2))
        grayEqCrop = cv2.resize(grayEq, newdim, interpolation = cv2.INTER_AREA)
        
        if debug:
            cv2.imshow('Processamento Demo', grayEqCrop)
            cv2.waitKey(50)


        #Aplica Blur pra remover ruido de alta freq
        blurred = cv2.GaussianBlur(grayEqCrop, (3, 3), 0)
        
        if debug:
            cv2.imshow('Processamento Demo', blurred)
            cv2.waitKey(50)


        #Aplicando o Threshold para evidenciar os pontos
        #neste Caso, pode-se calibrar o valor. 200 eh a base
        thresh = cv2.threshold(blurred, 190, 255, cv2.THRESH_BINARY)[1]
        
        if debug:
            cv2.imshow('Processamento Demo', thresh)
            cv2.waitKey(50)


        #Performando uma análise de componentes conectados, para gerar uma máscara de blobls
        labels = measure.label(thresh, connectivity=2, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")


        # loop sobre os blobs para eliminar blobs pequenos e muito grandes
        minBlob = 100 # variaveis de controle
        maxBlob = 600 # variaveis de controle
        
        if debug:
            print( 'minimo blob:' + str(minBlob) )
            print( 'maximo blob: ' + str(maxBlob) )
        
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue
        
            # otherwise, construct the label mask and count the
            # number of pixels 
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
        
            #Se o número de pixels dentro do blob estiver dentro dum limite, ele é add
            if numPixels > minBlob and numPixels < maxBlob: 
                #o tamanho dos blobs que ficam controla-se por aqui, o 500 eh para eliminar grandes blobls
                mask = cv2.add(mask, labelMask)
        
        if debug:
            cv2.imshow('Processamento Demo', mask)
            cv2.waitKey(50)



        #Acha os contornos na imagem
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)



        # iterando sobre os contornos
        pts =[] #lista de pontos que vão ser selecionados
        for c in cnts:
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            if radius > 4 and radius < 15: #controle do tamanho dos pontos que serão detectados, pelo raio 
                if cX > 100 and cX < grayEqCrop.shape[1] - 100: #comi 100px de cada lado da imagem pra concentrar os pontos no centro da face
                    if cY > 100 and cY < grayEqCrop.shape[0] - 100:
                        cv2.circle(grayEqCrop, (int(cX), int(cY)), int(radius),
                                (0, 0, 255), 2)
                        pts.append((cX, cY)) #salva os pontos em pts
        if debug:
            cv2.imshow("Processamento Demo", grayEqCrop)
            cv2.waitKey(50)

            print('Pontos Encontrados:' + str(len(pts)))



        #processo de análise de linhas individuais (os pontos são escaneados pelo CV da esquerda pra direita, cima pra baixo)
        #como numa varredura. Irei percorrer os pontos até que haja uma grande variação no valor y, aí eu saberei que a linha
        #mudou para uma linha mais abaixo. Pequenas variações em Y devem ser toleradas devido ao entortamento da linha
        last_Y = 0
        num_linhas = 0
        first_iteration = True
        line_change = False
        lista_y_das_linhas = [] #lista com os valores de Y dos pontos da linha X, a variancia desses valores de Y determinará o entortamento dela
        temp_x_list = [] #listas temporarias pro meu plot
        temp_y_list = []
        for  (x,y) in pts:
            if not first_iteration:
                if line_change: #ao mudar a linha, salva-se a lista temporaria de pontos Y na lista principal (lista de listas, uma lista por linha)
                    lista_y_das_linhas.append(temp_y_list)
                    if debug:
                        plt.plot(temp_x_list, temp_y_list) #plota-se os pontos daquela linha (para a cor ficar univorme)
                        plt.scatter(temp_x_list[:],temp_y_list[:] ) #coloca a dispersão dos pontos daquela linha (cor tb uniforme)

                    temp_x_list = [] #esvaziando as listas para a próxima linha
                    temp_y_list = []
                    temp_x_list.append(x)
                    temp_y_list.append(y)
                    line_change = False
                else: #ainda dentro da mesma linha
                    if abs(last_Y - y) < 8:  # isso significa que Y variou pouco, ou seja, estamos na mesma linha
                        temp_x_list.append(x) # salva a coordenada x conforme percorre os pontos da linha
                        temp_y_list.append(y)
                    else: #trigger de mudança de linha
                        num_linhas += 1 
                        line_change = True
            last_Y = y #sempre salvar o ultimo valor de Y o ultimo ponto analizado para avaliar o delta
            first_iteration  = False

        if debug:
            print ('Linhas Encontradas: ' + str(num_linhas))



        # Cálculo da Variância por linha e total
        totalvar = 0 #variancia acumulada, usado pra calcular media
        for i in range(num_linhas):
            varlinha = np.var(lista_y_das_linhas[i])
            if debug:
                print ('Variancia Linha ' + str(i+1) + ': ' + str(varlinha) + '\n') #calcula variância dos Ys da linha
            
            if varlinha > 0:
                totalvar += varlinha #acumula nessa variavel
            else:
                num_linhas -= 1

        totalvar = totalvar / num_linhas #tira a média

        if debug:
            print ('Variancia total Media')
            print (totalvar)


        colorEqCrop = cv2.cvtColor(grayEqCrop,cv2.COLOR_GRAY2RGB) #convertendo minha grayEqCrop para imagem colorida

        #printando os resultados
        if totalvar > 10:
            if debug:
                print ('SUCESSO!')
                cv2.putText(colorEqCrop, 'SUCESSO NA PROVA DE VIDA', (80, 750), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 180, 0), 6)
            result = True
        else:
            if debug:
                print ('FALHA')
                cv2.putText(colorEqCrop, 'FALHA NA PROVA DE VIDA', (100, 750), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 180), 6)
            result = False

        if debug:
            cv2.imshow("Processamento Demo", colorEqCrop)
            cv2.waitKey(50)
            plt.show() #mostrando a análise dos pontos de forma gráfica

        return result