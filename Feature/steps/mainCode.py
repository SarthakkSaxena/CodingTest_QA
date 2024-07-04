import json
import os

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from Pages import LoginPage, DemoPage, checkoutPage

path = os.getcwd()

# Environment Data
with open(path + '/Feature/EnvironmentData.json') as file:
    EnvironmentData = json.load(file)
    demoPageUrl = EnvironmentData['demoPageUrl']
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def login(userName, password):
    driver.find_element(By.XPATH, LoginPage.LoginPageElements['username']).send_keys(userName)
    driver.find_element(By.XPATH, LoginPage.LoginPageElements['password']).send_keys(password)


@given('I am on the Demo Login Page')
def loginpage(context):
    # Visiting the login page
    driver.get(EnvironmentData['BaseUrl'])


@when('I fill the account information for account StandardUser into the Username field and the Password field')
def Username_password(context):
    # Login Function
    login(EnvironmentData['user1Name'], EnvironmentData['commonPassword'])


@when('I click the Login Button')
def loginButton(context):
    driver.find_element(By.XPATH, LoginPage.LoginPageElements['loginButton']).click()


@then('I am redirected to the Demo Main Page')
def demoMainPage(context):
    assert demoPageUrl == driver.current_url


@then('I verify the App Logo exists')
def logoVerification(context):
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['appLogo']).is_displayed()
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['appLogo']).text == EnvironmentData['App_logo']


@when('I fill the account information for account LockedOutUser into the Username field and the Password field')
def failedLoginCredentials(context):
    login(EnvironmentData['user2Name'], EnvironmentData['commonPassword'])


@then('I verify the Error Message contains the text "Sorry, this user has been banned. "')
def validating_errorMessage_locked_out_user(context):
    print('actual-->', driver.find_element(By.XPATH, LoginPage.LoginPageElements['Errormessage']).text)
    print('expected-->', EnvironmentData['errorMessage_for_lockedOut_User'])
    assert driver.find_element(By.XPATH, LoginPage.LoginPageElements['Errormessage']).text.__contains__(EnvironmentData['errorMessage_for_lockedOut_User'])


@given('I am on the inventory page')
def navigating_to_inventory_page(context):
    # Logging In and Validating I am on inventory page
    driver.get(EnvironmentData['BaseUrl'])
    login(EnvironmentData['user1Name'], EnvironmentData['commonPassword'])
    driver.find_element(By.XPATH, LoginPage.LoginPageElements['loginButton']).click()

    # Logging In and Validating I am on inventory page
    assert driver.find_element(By.XPATH,  DemoPage.DemoPageElements['appLogo']).is_displayed()


@when('user sorts products from low price to high price')
def sorting_InventoryPage(context):
    driver.find_element(By.XPATH, DemoPage.DemoPageElements['productSortContainer']).click()
    driver.find_element(By.XPATH, DemoPage.DemoPageElements['lowToHigh']).click()

    # Function for getting item price
    elem = driver.find_elements(By.XPATH, DemoPage.DemoPageElements['InventoryPriceTag'])
    values = []
    for ele in elem:
        ele = ele.text
        ele = float(ele.replace('$', ""))
        values.append(ele)
    minimumValue = '$' + str(min(values))

    assert minimumValue == EnvironmentData['minimumValue']


@when('user adds lowest priced product')
def userClicksOnLowestPriceProduct(context):
    global selecteditemtitle, selecteditemLabel
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['addToCartIcon']).text == EnvironmentData['addToCart_label']
    # Storing Values of selected item
    selecteditemtitle = driver.find_element(By.XPATH,
                                            DemoPage.DemoPageElements['inventoryItemName']).text
    selecteditemLabel = driver.find_element(By.XPATH, DemoPage.DemoPageElements['inventoryItemDescription']).text

    driver.find_element(By.XPATH, DemoPage.DemoPageElements['inventoryItem_titleLink']).click()
    driver.find_element(By.XPATH, DemoPage.DemoPageElements['addToCartIcon_byId']).click()

    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['removeButton']).text == EnvironmentData['Remove_label']


@when('user clicks on cart')
def userClicksOnCart(context):
    assert driver.find_element(By.XPATH,
                               DemoPage.DemoPageElements['cartIcon_value']).text == '1'
    driver.find_element(By.XPATH, DemoPage.DemoPageElements['shoppingCart_icon']).click()


@when('user clicks on checkout')
def userClicksOnCheckout(context):
    assert EnvironmentData['cartPageUrl'] == driver.current_url
    assert driver.find_element(By.XPATH, checkoutPage.cartElements['CheckoutButton']).text == EnvironmentData['Checkout']

    driver.find_element(By.XPATH, checkoutPage.cartElements['CheckoutButton']).click()


@when('user enters first name John')
def userEntersFirstName(context):
    assert EnvironmentData['checkoutStepOneUrl'] == driver.current_url
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['firstName_textBox']).get_attribute('placeholder') == EnvironmentData['firstName_label']
    driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['firstName_textBox']).send_keys('John')


@when('user enters last name Doe')
def userEntersLastName(context):
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['lastName_textBox']).get_attribute('placeholder') == 'Last Name'
    driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['lastName_textBox']).send_keys('Doe')


@when('user enters zip code 123')
def userEntersZipcode(context):
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['ZipPostalCode_textBox']).get_attribute(
        'placeholder') == EnvironmentData['ZipPostal_label']
    driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['ZipPostalCode_textBox']).send_keys('123')


@when('user clicks Continue button')
def userClicksOnContinueButton(context):
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['continueButton']).get_attribute('value') == EnvironmentData['Continue_Label']
    driver.find_element(By.XPATH, checkoutPage.checkoutPageOne['continueButton']).click()


@then('I verify in Checkout overview page if the total amount for the added item is $8.63')
def verifyCheckoutPage(context):
    assert EnvironmentData['checkoutStepTwoUrl'] == driver.current_url
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['title']).text == EnvironmentData['Checkout_label']
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['Quantity']).text == EnvironmentData['Quantity_label']
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['description']).text == EnvironmentData['description_label']
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['paymentInformation']).text == EnvironmentData['paymentInformation_label']
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['shippingInformation']).text == EnvironmentData['shippingInformation']

    assert driver.find_element(By.XPATH,
                               checkoutPage.checkoutPageTwo['quantityValue']).text == '1'
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['inventoryItemName']).text == selecteditemtitle
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['inventoryItemDescription']).text == selecteditemLabel
    assert driver.find_element(By.XPATH, DemoPage.DemoPageElements['InventoryPriceTag']).text == '$7.99'

    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['totalPriceLabel']).text == EnvironmentData['totalPrice']

    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['subTotal']).text == 'Item total: $7.99'
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['taxLabel']).text == 'Tax: $0.64'

    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['totalLabel']).text == 'Total: $8.63'


@when('user clicks Finish button')
def userclickFinishbutton(context):
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['finish']).text == EnvironmentData['finishLabel']
    driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['finish']).click()


@then('Thank You header is shown in Checkout Complete page')
def CheckoutCompleted(context):
    assert EnvironmentData['CheckoutCompletedUrl'] == driver.current_url
    driver.find_element(By.XPATH, checkoutPage.checkCompleted['completedLogo']).is_displayed()
    assert driver.find_element(By.XPATH, checkoutPage.checkoutPageTwo['title']).text == EnvironmentData['checkoutCompleted']
    assert driver.find_element(By.XPATH, checkoutPage.checkCompleted['completedHeader']).text == EnvironmentData['thankYou_message']
    assert driver.find_element(By.XPATH,
                               checkoutPage.checkCompleted['completedText']).text == EnvironmentData['dispatchedMessage']
    assert driver.find_element(By.XPATH, checkoutPage.checkCompleted['backHome']).text == EnvironmentData['backHome_label']

    driver.find_element(By.XPATH, checkoutPage.checkCompleted['backHome']).click()

    assert EnvironmentData['demoPageUrl'] == driver.current_url