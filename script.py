import math
import time
import matplotlib.pyplot as plt
import requests
import concurrent.futures


def calcular_onda_seno( ):
    # Número de puntos en la onda
    num_puntos = 100
    periodo = 20  # Grados en un periodo completo de la onda seno
    ang = -1
    scale = 100
    t_sleep = 0
    # Calcular la onda seno
    onda_seno = []
    for i in range(num_puntos):
        ang = ( (ang + 1 ) % periodo )
        punto = abs(scale * math.sin(  2* math.pi * ( ang/periodo ) ))  + 1 
        onda_seno.append(punto)
        #print(punto)
    return onda_seno

def hacer_peticion(url):
    try:
        response = requests.get(url)
        print(f"Página {url} obtenida con éxito - Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al obtener la página {url}: {str(e)}")

def graficar_onda_seno(onda_seno_calculada):
    num_puntos = len(onda_seno_calculada)
    x_vals = range(num_puntos)

    plt.plot(x_vals, onda_seno_calculada)
    plt.title('Onda Seno Calculada')
    plt.xlabel('Puntos')
    plt.ylabel('Valor')
    plt.show()


def main():
    delay_time = 5
    url = "http://127.0.0.1:8080/memory"
    # Calcular la onda seno con el factor de escala proporcionado
    onda_seno_calculada = calcular_onda_seno()

    for num_peticiones in onda_seno_calculada:
        num_peticiones = int( num_peticiones)
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_peticiones) as executor:
        # Repite la función hacer_peticion con la misma URL num_peticiones veces
            executor.map(hacer_peticion, [url] * num_peticiones)
            time.sleep(delay_time)
    # Imprimir la onda seno calculada
    print("Onda Seno Calculada:")


    graficar_onda_seno(onda_seno_calculada)
    print(onda_seno_calculada)


if __name__ == "__main__":
    main()
