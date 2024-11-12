# from behave import *
# from selenium import webdriver
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from behave_basics.components.base import Base
#
# @step('Navigate to {url}')
# def step_impl(context, url):
#     context.browser.get(url)
#
# @when("Search for {search_item}")
# def step_impl(context, search_item):
#     base = Base(context.browser)
#     # search_xpath = '//input[@data-test="@web/Search/SearchInput"]'
#     search_id = (By.ID, "search")
#     base.find_element(search_id).send_keys(search_item, Keys.RETURN)
#
# @then("Verify header of the page contains {search_item}")
# def step_impl(context, search_item):
#     base = Base(context.browser)
#     try:
#         header_items = base.find_element((By.XPATH, '//h1[@data-test="page-title"]'))
#     except:
#         # header_items = base.find_element((By.XPATH, '//div[@data-test="resultsHeading"]/span')).text
#         header_items = base.find_element((By.XPATH, '//span[@class="h-text-bs h-display-flex h-flex-align-center h-text-grayDark h-margin-l-x2"]'))
#
#     assert search_item.lower() in header_items.text.lower(), f'{search_item} not found in {header_items.text}'
#
#     # base.find_element((By.XPATH, header_gift_ideas))
#
#     # return search_item == header


from behave import *
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from behave_basics.components.base import Base


@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    print_current_url(context)


@step('Print the current url')
def print_current_url(context):
    print("Current URL:", context.browser.current_url)


@step('Search for {search_item}')
def step_impl(context, search_item):
    base = Base(context.browser)
    search_field = (By.ID, "search")
    search_button = (By.XPATH, "//button[@class='sc-1c2974c-3 bsiIIZ']")
    base.find_element(search_field).send_keys(search_item)
    base.click(search_button)


@step('Verify header of the page contains {search_item}')
def step_impl(context, search_item):
    base = Base(context.browser)
    try:
        page_header = base.find_element(
            (By.XPATH, "//span[@class='h-text-bs h-display-flex h-flex-align-center h-text-grayDark h-margin-l-x2']"))
    except:
        page_header = base.find_element((By.XPATH, "//h1[@data-test='page-title']"))

    # page_header = base.find_element((By.XPATH, "//div[@data-test='resultsHeading']/span | //h1[not(@tabindex='-1')]"))
    assert search_item.lower() in page_header.text.lower(), f"Expected  {search_item} in header, but instead got {page_header.text} in header"


@when("Select {option} in {section} section")
def step_impl(context, section, option):
    base = Base(context.browser)
    section_selector = f"//div[.//span[text()='{section}']]"
    option_selector = f"{section_selector}//span[text()='{option}']"
    base.click((By.XPATH, option_selector))


@step('Collect all items on the first page into {context_var}')
@step('Collect all items on the first page into {context_var} on the {level} level')
def step_impl(context, context_var, level=None):
    base = Base(context.browser)
    context.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    item_headers = base.find_elements((By.XPATH, "//div[@class='h-display-flex h-flex-justify-space-between']"))
    context.collected_items = []

    for header in item_headers:
        parent_elem = header.find_element(By.XPATH,
                                          "./ancestor::div[@class='sc-5da3fdcc-0 iwPybp sc-87cbc592-0 hfGzVz']")
        price = parent_elem.find_element(By.XPATH, ".//span[@data-test='current-price']")
        price_str = price.text.split('(')[0].replace('$', '').replace(',', '').strip()

        if '-' in price_str:
            price_str = price_str.split('-')[0].strip()

        try:
            price_float = float(price_str)
        except ValueError:
            price_float = 0.0

        context.collected_items.append({
            'item_text': header.text,
            'price': price_float,
        })

    if level == "feature":
        setattr(context.feature, context_var, context.collected_items)


@step("Verify all collected results' {param} is {condition}")
def step_impl(context, param, condition):
    if param.lower() == "price":
        print(context.table)
        for item in context.table.headings:
            collected_items = getattr(context, item)
            print(collected_items)
            price = item['price']
            if not eval(f"{price} {condition}"):
                raise AssertionError(
                    f"Price of item '{item['item_text']}' is {price}, which does not meet the condition '{condition}'")
            print(f"All collected results' prices meet the condition '{condition}'")
