from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

service = ChromeService(executable_path=ChromeDriverManager().install())
options = ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options, service=service)


