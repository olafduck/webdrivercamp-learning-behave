from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class Base:

   def __init__(self, driver):
       self.driver = driver
       self.wait = WebDriverWait(driver, 10)

   def click(self, locator):
        elem = self.wait.until(expected_conditions.element_to_be_clickable(locator))
        elem.click()

   def find_element(self, locator):
        return self.wait.until(expected_conditions.element_to_be_clickable(locator))

   def find_elements(self, locator):
       elems = self.driver.find_elements(*locator)
       return elems