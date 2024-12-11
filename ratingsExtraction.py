import pandas as pd
import requests

# Tu API key de Google Cloud para acceder a Google Places API
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxx'

# Función para buscar el negocio en Google Places y obtener reseñas
def obtener_resenas_google(nombre_negocio):
    # Construir la URL de búsqueda en Google Places
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={nombre_negocio}&inputtype=textquery&fields=place_id,name,rating,user_ratings_total&key={API_KEY}"
    
    # Realizar la solicitud
    response = requests.get(url)
    datos = response.json()
    
    # Si encuentra un lugar, devolver el rating y el número de reseñas
    if 'candidates' in datos and len(datos['candidates']) > 0:
        lugar = datos['candidates'][0]
        return {
            'nombre': lugar['name'],
            'rating': lugar.get('rating', 'N/A'),
            'reseñas': lugar.get('user_ratings_total', 'N/A')
        }
    else:
        return {
            'nombre': nombre_negocio,
            'rating': 'No encontrado',
            'reseñas': 'No encontrado'
        }

# Leer los archivos CSV
def leer_csv(ruta_csv):
    return pd.read_csv(ruta_csv)

# Guardar resultados en un nuevo CSV
def guardar_resultados(resultados, nombre_archivo):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(nombre_archivo, index=False)

# Procesar cada negocio de los CSV
def procesar_negocios(csv1, csv2):
    # Leer ambos CSVs
    tabla1 = leer_csv(csv1)
    tabla2 = leer_csv(csv2)
    
    # Unir ambas tablas (si corresponde, puedes cambiar el tipo de unión según tus necesidades)
    tabla_completa = pd.concat([tabla1, tabla2])

    # Columna que contiene los nombres de los negocios
    columna_negocios = 'Dirección'  # Cambia esto según el nombre de la columna en tu CSV
    
    resultados = []
    
    # Para cada negocio en la columna
    for negocio in tabla_completa[columna_negocios]:
        resultado = obtener_resenas_google(negocio)
        resultados.append(resultado)
    
    # Guardar los resultados en un nuevo archivo CSV
    guardar_resultados(resultados, 'resultados_resenas.csv')

# Ejecutar el script
if __name__ == '__main__':
    csv1 = 'peluquerias_caninas_madrid_zonas.csv'  # Cambia por la ruta de tu primer archivo CSV
    csv2 = 'veterinarios_caninas_madrid_zonas.csv'  # Cambia por la ruta de tu segundo archivo CSV
    
    procesar_negocios(csv1, csv2)
