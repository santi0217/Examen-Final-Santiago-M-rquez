import os
from hough import *
from orientation_estimate import *
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

class Bandera:

    #constructor de la clase
    def __init__(self):
        path = input('Ingrese la ruta en su PC de la carpeta donde esta la imagen a procesar: ')
        image_name = input('Ingrese el nombre de su imagen: ')
        image_path = os.path.join(path, image_name)
        self.image_ = cv2.imread(image_path)  # lee la imagen y la almacena en self.image

    #funcion que retorna el numero de colores de la imagen
    def Colores(self):
        self.image = self.image_.copy()
        RGB_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # convierte la imagen BGR modificada a RGB

        # Se hace casting a los datos de la imagen y se normaliza
        self.image = np.array(RGB_image, dtype=np.float64) / 255

        # se define el numero maximo de clusters
        n_colors = 4
        # se redimensiona la imagen a 2D para el metodo KMeans
        rows, cols, ch = self.image.shape
        image_array = np.reshape(self.image, (rows * cols, ch))

        #se muestrea aleatoriamente la imagen para crear el modelo KMeans
        image_array_sample = shuffle(image_array, random_state=0)[:1000]
        model = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)

        # se generan las etiquetas de cada pixel
        self.labels = model.predict(image_array)

        #devido al warning de los duplicados se observa cual etiqueta o cluster tiene pixeles y cual no
        min_label = min(self.labels)
        max_label = max(self.labels)
        print(min_label,max_label)

        # se retorna el numero de clusters o colores de la imagen
        return (max_label-min_label+1)

    #funcion que retorna el porcentaje de cada color en la imagen
    def Porcentaje(self):
        porcentajes = [0, 0, 0, 0]
        #se recorreo el arreglo de etiquetas para saber cuantos pixeles estan en cada etiqueta
        for i in range(len(self.labels)):
            if self.labels[i] == 0:
                porcentajes[0] += 1
            if self.labels[i] == 1:
                porcentajes[1] += 1
            if self.labels[i] == 2:
                porcentajes[2] += 1
            if self.labels[i] == 3:
                porcentajes[3] += 1
        #se calcula el porcentaje de cada frecuencia calculada por color y retorno el arreglo de porcentajes
        for i in range(len(porcentajes)):
            porcentajes[i] = (porcentajes[i]*100/len(self.labels))
        return porcentajes

    #funcion que retorna la orientacion de la bandera en la imagen
    def Orientacion(self):
        high_thresh = 300
        bw_edges = cv2.Canny(self.image_, high_thresh * 0.3, high_thresh, L2gradient=True)

        hough_ = hough(bw_edges)
        accumulator = hough_.standard_HT()

        acc_thresh = 50
        N_peaks = 5
        nhood = [25, 9]
        peaks = hough_.find_peaks(accumulator, nhood, acc_thresh, N_peaks)

        [_, cols] = self.image_.shape[:2]
        image_draw = np.copy(self.image_)
        horizontal = 0
        vertical = 0
        for i in range(len(peaks)):
            rho = peaks[i][0]
            theta_ = hough_.theta[peaks[i][1]]

            theta_pi = np.pi * theta_ / 180
            theta_ = theta_ - 180
            a = np.cos(theta_pi)
            b = np.sin(theta_pi)
            x0 = a * rho + hough_.center_x
            y0 = b * rho + hough_.center_y
            c = -rho
            x1 = int(round(x0 + cols * (-b)))
            y1 = int(round(y0 + cols * a))
            x2 = int(round(x0 - cols * (-b)))
            y2 = int(round(y0 - cols * a))

            if np.abs(theta_) < 80:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 255, 255], thickness=2)
                vertical += 1
            elif np.abs(theta_) > 100:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [255, 0, 255], thickness=2)
            else:
                if theta_ > 0:
                    image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 255, 0], thickness=2)
                    horizontal += 1
                else:
                    image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)
                    horizontal += 1

        if horizontal != 0:
            if vertical != 0:
                return 'Mixta'
            else:
                return 'horizontal'
        else:
            return 'vertical'
