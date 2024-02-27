from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

url_lista_noticias = 'https://consumer.ftc.gov/articles'

# Función para extraer y traducir una noticia
def procesar_noticia(url_noticia, index):
    driver.get(url_noticia)

    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dialog-off-canvas-main-canvas')))

    noticia_original = driver.find_element(By.XPATH, '//*[@id="content"]').text
    
    nombre_archivo = f'noticia_es_{index + 1}.txt'
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(noticia_original)

    boton_espanol = driver.find_element(By.CLASS_NAME, 'language-link')
    boton_espanol.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dialog-off-canvas-main-canvas')))

    noticia_traducida = driver.find_element(By.XPATH, '//*[@id="content"]').text

    nombre_archivo = f'noticia_en_{index + 1}.txt'

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(noticia_traducida)

# Navegar por la lista de noticias
driver.get(url_lista_noticias)

# Supongamos que las noticias están en una lista con enlaces únicos
enlaces_noticias = driver.find_elements(By.CLASS_NAME, 'node__content')

for index, enlace in enumerate(enlaces_noticias):
    elemento_noticia = enlace.find_element(By.CSS_SELECTOR, 'h3')
    tag_noticia = elemento_noticia.find_element(By.CSS_SELECTOR, 'a')
    url_noticia = tag_noticia.get_attribute('href')
    procesar_noticia(url_noticia, index)

driver.quit()