from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
from time import sleep

# Scrolling Javascript
def getScrollingScript(iteration) : 
    scrollingScript = """
        document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 100000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

opts = Options()
# Configuracion de User Agent
opts.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36')
# Instancia de Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
# URL
driver.get('https://www.google.com/maps/place/Roof+Burger/@-33.0169979,-71.5559245,16.52z/data=!4m7!3m6!1s0x9689dde432c2e655:0x5a8b567480037ae5!8m2!3d-33.0166854!4d-71.5553927!9m1!1b1')
# Espera de carga de website
sleep(random.uniform(4,5))
## Scroling para obtener data dinamica
scrolls = 0
while(scrolls != 3) :
    driver.execute_script(getScrollingScript(scrolls))
    sleep(random.uniform(5, 6))
    scrolls += 1
# Obtener los reviews
reviews = driver.find_elements(By.XPATH, '//div[@data-review-id and @aria-label]')
# Iterar reviews
for review in reviews :
    # Obtener el link del usuario
    userLink = review.find_element(By.XPATH, './/div[@class="WNxzHc qLhwHc"]')
    try :
        # Abrir el linl del usuario
        userLink.click()
        # Pasar a nueva pestaña
        driver.switch_to.window(driver.window_handles[1])
        # Esperar que este las reviews esten disponibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc"]'))
        )
        # Scrolling
        scrolls = 0
        while(scrolls != 3) :
            driver.execute_script(getScrollingScript(scrolls))
            sleep(random.uniform(5, 6))
            scrolls += 1
        # Obtener el usuario 
        user = driver.find_element(By.XPATH, '//h1[@class="geAzIe F8kQwb"]').text
        print('===> User : ', user)
        # Obtener todos los reviews
        user_reiviews = driver.find_elements(By.XPATH, '//div[@aria-label and @data-review-id]')
        # //div[contains(@class, "fontBodyMedium")]
        for user_review in user_reiviews :
            store = user_review.find_element(By.XPATH, './/div[@class="ODSEW-ShBeI-title YJxk2d"]//span').text
            print('Store : ', store)
            rating = user_review.find_element(By.XPATH, './/span[@class="ODSEW-ShBeI-H1e3jb"]').get_attribute('aria-label')
            print('Rating : ', rating)
        # Cerrar usuario
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e :
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])