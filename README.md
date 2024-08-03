# Python-Selenium
Netflix Web Automation

Netflix Log Checker:

* The netflix function processes user inputs received through the bot.
* User messages are split into components to extract email and password pairs.
* A check ensures that the input format is correct (at least one email-password pair).

Automation Process:

* The function calculates the number of email-password sets provided.
* A loop iterates through each set to perform the login check.
* Using selenium.webdriver.Chrome, the script initiates a Chrome browser session.
* It tracks the start time and initializes an empty list for messages.

Login and Check:

* The script likely uses Selenium to navigate to Netflix, enter the email and password, and perform login actions.
* It checks the login success and retrieves details like billing information, next billing date, and the plan associated with the account.

Feedback to User:

* Based on the retrieved information, the bot sends a message back to the user via Telegram, informing them of the login success and the account details.

--> The purpose of this script is to automate the process of checking Netflix account details using provided email and password combinations, and then informing the user of the status and details of their accounts through a Telegram bot.
## Preview
![Success](https://github.com/DiwakarG-12/Python-Selenium/blob/main/Success.gif)
