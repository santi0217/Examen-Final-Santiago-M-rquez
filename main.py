from Bandera import *

if __name__ == '__main__':
    while True:
        #inicializo la clase bandera para ingresar la imagen
        bandera = Bandera()

        #recibo el numero de colores de la bandera en la imagen y lo imprimo
        n_colores = bandera.Colores()
        print("La cantidad de colores de la bandera en la imagen es de:",n_colores)

        #recibo el porcentaje de cada color de la bandera en la imagen y lo impirmo
        porcentaje = bandera.Porcentaje()
        for i in range(len(porcentaje)):
            if porcentaje[i] != 0:
                print("El porcentaje del color ",i," es: ",porcentaje[i],"%")

        orientacion = bandera.Orientacion()
        print("La bandera tiene orientacion ", orientacion)