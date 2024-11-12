from selenium import webdriver

def before_feature(context, feature):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(10)

def after_feature(context, feature):
    context.browser.quit()