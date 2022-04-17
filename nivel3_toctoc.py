import random
from time import sleep
from tkinter import E
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# URL
driver.get('https://www.toctoc.com/arriendo/departamento/metropolitana/santiago')

# Obtener todos los departamentos
deptos = driver.find_elements_by_xpath('//li[@class="un-ress tp3"]')

# Crear boton de carga
btn = driver.find_element_by_xpath('//button[@id="btnCargarMas"]')

for i in range(3) :
    try: 
        # Click a boton de carga
        btn.click()
        # Recrear boton de carga
        btn = driver.find_element_by_xpath('//button[@id="btnCargarMas"]')
        # Espera para cargar más data
        sleep(random.uniform(8,10))
    except :
        break

for depto in deptos :
    titulo = depto.find_element_by_xpath('.//h3[@class="dir etc"]').text
    print(titulo)
    precio = depto.find_element_by_xpath('.//h4[1][@class="precio"]').text
    print(precio)