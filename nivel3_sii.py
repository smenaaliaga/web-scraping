from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

opts = Options()
# Configuracion de User Agent
opts.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36')
# Instancia de Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
# URL
driver.get('https://homer.sii.cl')
# Ingresar a Mi SII
btn = driver.find_element(By.XPATH, '//button[@data-dismiss="modal"]')
btn.click()
btn = driver.find_element(By.XPATH, '(//li[@class="special"])[1]')
btn.click()
btn = driver.find_element(By.XPATH, '(//li[@class="special"])[1]')
btn.click()
# Ingresar por medio de Clave Unica
btn = driver.find_element(By.XPATH, '//a[@onclick="callOne();"]')
btn.click()
# Credenciales
user = "190319105"
password = open('crypted.psw').readline().strip()
# Identificar elementos de credencial
input_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="uname"]'))
)
input_password = driver.find_element(By.XPATH, '//input[@id="pword"]')
# Enviar texto a los elementos de credenncial
input_user.send_keys(user)
input_password.send_keys(password)
# Obtener boton y enviar formulario de credencial
btn = driver.find_element(By.XPATH, '//button[@id="login-submit"]')
btn.click()
# Espera
sleep(20)