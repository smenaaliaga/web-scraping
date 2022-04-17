from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
from time import sleep

opts = Options()
# Configuracion de User Agent
opts.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36')
# Instancia de Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
# URL
driver.get('https://www.facebook.com/')
# Credenciales
user = "smenaaliaga@hotmail.com"
password = "seba1995"
# Identificar elementos de credencial
input_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="email"]'))
)
input_password = driver.find_element(By.XPATH, '//input[@type="password"]')
# Enviar texto a los elementos de credenncial
input_user.send_keys(user)
input_password.send_keys(password)
# Obtener boton y enviar formulario de credencial
btn = driver.find_element(By.XPATH, '//form[@data-testid="royal_login_form"]//button[@name="login"]')
btn.click()
# Espera
sleep(15)