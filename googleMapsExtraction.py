import requests
import pandas as pd
import time

# Tu API Key de Google Places
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'

# Definir el radio en metros
radius = 1000  # 1 km

# Función para realizar la búsqueda en una ubicación dada
def buscar_peluquerias(lat, lng, radius, keyword='peluquería canina'):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&key={API_KEY}'
    response = requests.get(url)
    return response.json()
def buscar_veterinarios(lat, lng, radius, keyword='veterinario'):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&key={API_KEY}'
    response = requests.get(url)
    return response.json()

# Coordenadas iniciales (Centro de Madrid)
lat_inicial = 40.416775  # Latitud de Madrid
lng_inicial = -3.703790  # Longitud de Madrid

# Desplazamiento en grados (aproximadamente 1 km ≈ 0.009 grados de latitud/longitud)
desplazamiento_lat = 0.009  # Equivalente a ~1 km de desplazamiento en latitud
desplazamiento_lng = 0.012  # Equivalente a ~1 km de desplazamiento en longitud (en Madrid)

# Definir el número de pasos en la cuadrícula
num_pasos = 5  # Cuadrícula de 5x5 (25 búsquedas en total)

# Lista para almacenar los resultados
lista_peluquerias = []
lista_veterinarios = []

# Iterar por una cuadrícula de latitudes y longitudes
for i in range(num_pasos):
    for j in range(num_pasos):
        # Recorremos hacia arriba y hacia la derecha
        lat_actual = lat_inicial + (i * desplazamiento_lat)
        lng_actual = lng_inicial + (j * desplazamiento_lng)
        
        # Buscar peluquerías en las coordenadas actuales
        resultados_peluquerias = buscar_peluquerias(lat_actual, lng_actual, radius)
        resultados_veterinarios = buscar_veterinarios(lat_actual, lng_actual, radius)
        # Extraer los datos relevantes de la respuesta
        for place in resultados_peluquerias.get('results', []):
            nombre = place.get('name')
            direccion = place.get('vicinity')
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            lista_peluquerias.append({'Nombre': nombre, 'Dirección': direccion, 'Latitud': lat, 'Longitud': lng})
        
        for place in resultados_veterinarios.get('results', []):
            nombre = place.get('name')
            direccion = place.get('vicinity')
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            lista_veterinarios.append({'Nombre': nombre, 'Dirección': direccion, 'Latitud': lat, 'Longitud': lng})

        # Recorremos hacia arriba y hacia la izquierda
        lat_actual = lat_inicial + (i * desplazamiento_lat)
        lng_actual = lng_inicial - (j * desplazamiento_lng)
        # Dormir un poco entre peticiones para evitar límites de tasa de la API

        # Buscar peluquerías en las coordenadas actuales
        resultados_peluquerias = buscar_peluquerias(lat_actual, lng_actual, radius)
        resultados_veterinarios = buscar_veterinarios(lat_actual, lng_actual, radius)
        # Extraer los datos relevantes de la respuesta
        for place in resultados_peluquerias.get('results', []):
            nombre = place.get('name')
            direccion = place.get('vicinity')
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            lista_peluquerias.append({'Nombre': nombre, 'Dirección': direccion, 'Latitud': lat, 'Longitud': lng})
        
        for place in resultados_veterinarios.get('results', []):
            nombre = place.get('name')
            direccion = place.get('vicinity')
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            lista_veterinarios.append({'Nombre': nombre, 'Dirección': direccion, 'Latitud': lat, 'Longitud': lng})
 
        time.sleep(2)

# Crear un DataFrame con los resultados
df_peluquerias = pd.DataFrame(lista_peluquerias)
df_veterinarios = pd.DataFrame(lista_veterinarios)

# Guardar los resultados en un archivo CSV
df_peluquerias.to_csv('peluquerias_caninas_madrid_zonas.csv', index=False)
df_veterinarios.to_csv('veterinarios_caninas_madrid_zonas.csv', index=False)

print(f"Se han encontrado {len(lista_peluquerias)} peluquerías y el listado está guardado en peluquerias_caninas_madrid_zonas.csv")
