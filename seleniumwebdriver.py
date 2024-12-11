from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Ruta donde está ubicado el ChromeDriver
PATH = "ruta/al/chromedriver"

# Inicializamos el navegador
driver = webdriver.Chrome(PATH)

# Accedemos a Google
driver.get("https://www.google.com")

# Esperamos un momento para que cargue la página
time.sleep(2)

# Encontramos la barra de búsqueda
search_bar = driver.find_element("name", "q")

# Escribimos el término de búsqueda
search_bar.send_keys("automatización con python")

# Presionamos Enter para buscar
search_bar.send_keys(Keys.RETURN)

# Esperamos a que carguen los resultados
time.sleep(5)

# Cerrar el navegador
driver.quit()