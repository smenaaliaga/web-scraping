from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

# URL
driver.get('https://www.toctoc.com/arriendo/departamento/metropolitana/santiago')

# Obtener todos los departamentos
deptos = driver.find_elements_by_xpath('//li[@class="un-ress tp3"]')

for i in range(3) :
    try: 
        # Instanciar boton de carga una vez exista
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="btnCargarMas"]'))
        )
        # Click a boton de carga
        btn.click() 
        # Esperar que se cargue la información cargada
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@class="un-ress tp3"]//h3[@class="dir etc"]'))
        )
    except :
        break

# Recorrer cada uno de los departamentos obtenidos
for depto in deptos :
    titulo = depto.find_element_by_xpath('.//h3[@class="dir etc"]').text
    print(titulo)
    precio = depto.find_element_by_xpath('.//h4[1][@class="precio"]').text
    print(precio)