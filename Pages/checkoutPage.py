cartElements = {
    "CheckoutButton": '//button[@data-test="checkout"]'
}

checkoutPageOne = {
    "firstName_textBox": '//input[@data-test="firstName"]',
    "lastName_textBox": '//input[@data-test="lastName"]',
    "ZipPostalCode_textBox": '//input[@data-test="postalCode"]',
    "continueButton": '//input[@data-test="continue"]'
}

checkoutPageTwo = {
    "title": '//span[@data-test="title"]',
    "Quantity": '//div[@data-test="cart-quantity-label"]',
    "description": '//div[@data-test="cart-desc-label"]',
    "paymentInformation": '//div[@data-test="payment-info-label"]',
    "shippingInformation": '//div[@data-test="shipping-info-label"]',
    "quantityValue": '//div[@data-test="inventory-item"]//div[@data-test="item-quantity"]',
    "totalPriceLabel": '//div[@data-test="total-info-label"]',
    "subTotal": '//div[@data-test="subtotal-label"]',
    "taxLabel": '//div[@data-test="tax-label"]',
    "totalLabel": '//div[@data-test="total-label"]',
    "finish": '//button[@data-test="finish"]'
}

checkCompleted = {
    "completedLogo" : '//img[@data-test="pony-express"]',
    "completedHeader" : '//h2[@data-test="complete-header"]',
    "completedText" : '//div[@data-test="complete-text"]',
    "backHome": '//button[@data-test="back-to-products"]'
}