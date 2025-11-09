import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

# Guardar datos en CSV con encabezados
def guardar_busqueda(nombre, capital, region, subregion, poblacion):
    archivo_nuevo = not os.path.exists("busquedas.csv")
    with open("busquedas.csv", mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if archivo_nuevo:
            escritor.writerow(["Nombre", "Capital", "Región", "Subregión", "Población"])
        escritor.writerow([nombre, capital, region, subregion, poblacion])

# Obtener datos del país desde la API
def obtener_informacion_pais(nombre_usuario):
    try:
        nombre_en_ingles = nombre_usuario  # Traducción desactivada por estabilidad
        url = f"https://restcountries.com/v3.1/name/{nombre_en_ingles}?fullText=true"
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            datos = respuesta.json()[0]

            nombre = datos['name']['common']
            capital = datos.get('capital', ['No disponible'])[0]
            region = datos.get('region', 'No disponible')
            subregion = datos.get('subregion', 'No disponible')
            poblacion = datos.get('population', 0)

            print("\nInformación del país:")
            print(f"Nombre: {nombre}")
            print(f"Capital: {capital}")
            print(f"Región: {region}")
            print(f"Subregión: {subregion}")
            print(f"Población: {poblacion}")

            guardar_busqueda(nombre, capital, region, subregion, poblacion)
        else:
            print("No se encontró información para ese país. Código:", respuesta.status_code)

    except Exception as e:
        print("Ocurrió un error al obtener la información:", e)

# Crear gráficos a partir del CSV
def generar_graficos():
    try:
        df = pd.read_csv("busquedas.csv", encoding="utf-8")

        if df.empty:
            print("No hay datos suficientes para generar gráficos.")
            return

        # Gráfico de barras: población por país
        plt.figure(figsize=(10, 5))
        plt.bar(df['Nombre'], df['Población'], color='skyblue')
        plt.xlabel("País")
        plt.ylabel("Población")
        plt.title("Población de países buscados")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Gráfico de pastel: distribución por región
        plt.figure(figsize=(7, 7))
        df['Región'].value_counts().plot.pie(autopct="%1.1f%%", colors=["gold", "lightgreen", "lightblue"])
        plt.title("Distribución de países por región")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No se encontró el archivo de búsquedas. Realiza al menos una búsqueda primero.")
    except Exception as e:
        print("Error al generar los gráficos:", e)

# Menú principal
def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Buscar país")
        print("2. Mostrar gráficos de búsquedas")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            pais = input("Escribe el nombre del país en inglés (por ejemplo: Mexico, Peru, Brazil): ")
            obtener_informacion_pais(pais)
        elif opcion == '2':
            generar_graficos()
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Ejecutar el programa
menu()