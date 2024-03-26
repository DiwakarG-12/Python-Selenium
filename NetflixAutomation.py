import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = 'Your Token'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Bot is ready to execute the code.")

def netflix(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_input = user_message.split()

    if len(user_input) < 3 or len(user_input) % 2 == 0: 
        update.message.reply_text("Please provide at least one set of email and password in this format: /netflix email1 password1 [email2 password2 ...]")
        return

    num_sets = (len(user_input) - 1) // 2
    messages_list = []

    for i in range(num_sets):
        email = user_input[i * 2 + 1]
        password = user_input[i * 2 + 2]

        browser = webdriver.Chrome()
        start_time = time.time()
        messages = []

        try:
            browser.get("https://www.netflix.com/login") 
            wait = WebDriverWait(browser, 7)
            
            email_field = wait.until(EC.presence_of_element_located((By.ID, "id_userLoginId")))
            password_field = wait.until(EC.presence_of_element_located((By.ID, "id_password")))

            email_field.send_keys(email)
            password_field.send_keys(password)

            sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-uia='login-submit-button']")))
            sign_in_button.click()
            try:
             error_message_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]')))
             messages.append("email:"+email)
             messages.append("password:"+password)
             messages.append("Login Failed: " + error_message_element.text)

            except:
             messages.append("email:"+email)
             messages.append("password:"+password)
             messages.append("Login Successful!")
             browser.get("https://www.netflix.com/BillingActivity")
             try:
                 bill_data = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/section/div')))
                 messages.append("Billing Data: " + bill_data.text)
             except:
                 messages.append("No Recent Billing Data Found. Account is not active")
             try:
                browser.get("https://www.netflix.com/logout")
                sign_out_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div[2]/a[2]')))
                sign_out_button.click()
                messages.append("❗️NOTE:- The Data You Provided is Encrypted in Our Servers")
                messages.append("Logout Successful!")

             except:
                messages.append("Error during logout")
                update.message.reply_text("There was an error during logout.")
        finally:
         browser.quit()
         
        end_time = time.time() - start_time
        messages.append(f"Execution time: {int(end_time)} seconds")
        message = "\n".join(messages)
        update.message.reply_text(message)


def aha(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_input = user_message.split()

    if len(user_input) < 3 and (len(user_input)%2) and (user_input=="/aha")== 0:  
        update.message.reply_text("Please provide at least one set of email and password in this format: /aha email1 password1 [email2 password2 ...]")
        return
    update.message.reply_text("Bot is on RUN...")
    num_sets = (len(user_input) - 1) // 2

    for i in range(num_sets):
        email = user_input[i * 2 + 1]
        password = user_input[i * 2 + 2]

        browser = webdriver.Chrome()
        start_time = time.time()
        messages = []

        try:
            browser = webdriver.Chrome()
            browser.get("https://www.aha.video/app/login")

            wait = WebDriverWait(browser, 5)
            #Proceed Selector
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-dialog-0"]/app-language-onboarding/div/section/section[2]/div[3]/div'))).click()
            #Mail Selector
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/app-root/div/app-login/div/div[2]/div/div[3]/div[7]/div[2]/div[1]'))).click()

            email_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/app-root/div/app-login/div/div[2]/div/div[6]/form/div[1]/input')))
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)

            pass_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/app-root/div/app-login/div/div[2]/div/div[6]/form/div[2]/div[2]/input')))
            pass_field.send_keys(password)
            pass_field.send_keys(Keys.RETURN)
            try:
             login_error = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/app-root/div/app-login/div/div[2]/div/div[6]/form/div[8]")))
             messages.append("Email:"+email)
             messages.append("Password:"+password)
             messages.append("Login Failed!")
             messages.append(login_error.text)
            except:
             messages.append("Email:"+email)
             messages.append("Password:"+password)
             messages.append("Login Successful!")
             try:
                 limit_error = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/app-root/div/app-login/div/div[2]/app-report-abuse/section/div[1]/h3')))
                 messages.append(limit_error.text)
             except:
                 browser.get("https://www.aha.video/account/subscription")
                 try:
                    billing = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/app-root/div/app-settings/section/div[2]/div/app-subscription/section')))
                    billing_text = billing.text
                    messages.append("Account is Active:✅")
                    messages.append("Billing Details:")
                    billing_lines = billing_text.split('\n')
                    for line in billing_lines[1:4]:
                     messages.append(line)
                 except:
                    messages.append("Accont is Inactive:❌")
                 try: 
                    # Move the mouse pointer to the user profile to make sub-options visible
                    profile_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="toolbar"]/div[2]/div[5]')))
                    actions = ActionChains(browser)
                    actions.move_to_element(profile_element).perform()
                    sub_options = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="users"]')))
                    browser.execute_script("arguments[0].scrollIntoView();", sub_options)
                    # Click on the logout option
                    logout_option = sub_options.find_element(By.XPATH, '//*[@id="users"]/app-users-card/div/div[2]/div[6]')
                    logout_option.click()
                    time.sleep(2)
                    update.message.reply_text("Logout is successful from the provided aha.video account.")

                 except Exception as e:
                    error_message = "An error occurred: " + str(e)
                    update.message.reply_text(error_message)
        finally:
         browser.quit()
         
        end_time = time.time() - start_time
        messages.append(f"Execution time: {int(end_time)} seconds")
        message = "\n".join(messages)
        update.message.reply_text(message)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("netflix", netflix))
    dispatcher.add_handler(CommandHandler("aha", aha))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
