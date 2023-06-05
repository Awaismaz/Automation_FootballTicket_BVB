from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QFormLayout, QDoubleSpinBox
import sys
from threading import Thread
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as webdriver
# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from twilio.rest import Client
driver = None

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('BVB Ticket Buyer')
        self.setGeometry(200, 200, 640, 300)

        layout = QVBoxLayout()


        form_layout = QFormLayout()

        self.label_email = QLabel("Email:")
        self.text_field_email = QLineEdit()

        self.label_password = QLabel("Password:")
        self.text_field_password = QLineEdit()
        self.text_field_password.setEchoMode(QLineEdit.Password)

        self.label_url = QLabel("Event URL")
        self.text_field_url = QLineEdit()

        self.whatsapp_label = QLabel("Whatsapp")
        self.whatsapp_number = QLineEdit()

        self.spinbox_label = QLabel("Clicks Delay (s)")
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(2)
        self.spinbox.setSingleStep(0.1)
        self.spinbox.setValue(0.1)

        form_layout.addRow(self.label_email, self.text_field_email)
        form_layout.addRow(self.label_password, self.text_field_password)
        form_layout.addRow(self.label_url, self.text_field_url)
        form_layout.addRow(self.spinbox_label, self.spinbox)
        form_layout.addRow(self.whatsapp_label, self.whatsapp_number)

        layout.addLayout(form_layout)

        

        self.button_start = QPushButton("Start")
        layout.addWidget(self.button_start)

        self.button_stop = QPushButton("Stop")
        layout.addWidget(self.button_stop)

        self.button_start.clicked.connect(self.start_bot)
        self.button_stop.clicked.connect(self.stop_bot)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.bot_thread = None
        self.stop_flag = False

        self.set_defaults()

    def set_defaults(self):
        self.text_field_url.setText("https://www.ticket-onlineshop.com/ols/bvb/de/bundesliga/channel/shop/index/index/event/460472")
        # self.text_field_url.setText("https://www.ticket-onlineshop.com/ols/bvb/de/handball/channel/shop/index/index/event/500020")
        self.text_field_email.setText("Default_email@domain.com")
        self.text_field_password.setText("Password")
        self.whatsapp_number.setText("Default Message Address")


    def start_bot(self):
        event_url = self.text_field_url.text()
        email = self.text_field_email.text()
        password = self.text_field_password.text()
        self.stop_flag = False
        self.bot_thread = Thread(target=self.run_bot, args=(event_url, email, password))
        self.bot_thread.start()

    def alert(self, contact, message):


        account_sid = 'AC0bc76f93de84c2e6833d3c86a0ab303e'
        auth_token = 'e8024481736f29d042734fdc87016f46'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:'+ contact
        )

        print(message.sid)

    def stop_bot(self):
        self.stop_flag = True

    def run_bot(self, event_url, email, password):
        global driver
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=C:\\Users\\awais\\AppData\\Local\\Google\\Chrome\\User Data')
        service = Service(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        driver = webdriver.Chrome(service=service)
        driver.get("https://account.bvb.de/s/login/?language=de")
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.ID, "centerPanel")))
        centerPanel=driver.find_element(By.ID, "centerPanel")
        form=centerPanel.find_element(By.TAG_NAME, 'form')
        time.sleep(1)
        username_element  = form.find_element(By.CSS_SELECTOR, "input.slds-input.username")
        password_element  = form.find_element(By.CSS_SELECTOR, "input.slds-input.password")
        username_element.send_keys(email)
        time.sleep(self.spinbox.value())
        password_element.send_keys(password)
        time.sleep(self.spinbox.value())
        password_element.send_keys(Keys.ENTER)

        wait.until(EC.url_changes("https://account.bvb.de/s/login/?language=de"))
        driver.get(event_url)

        # Wait for the cookie consent button to be clickable

        wait.until(EC.element_to_be_clickable((By.ID, "cookieConsentAgree")))

        # Find the cookie consent button and click on it
        cookie_button = driver.find_element(By.ID, "cookieConsentAgree")
        cookie_button.click()
        wait.until(EC.element_to_be_clickable((By.ID, "login-link")))

        # Find the link and click on it
        login_link = driver.find_element(By.ID, "login-link")
        login_link.click()

        wait = WebDriverWait(driver, 3)
        while not self.stop_flag:
            try:
                # Wait until the button is clickable
                wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button') and contains(@class, 'button--small') and contains(@class, 'button--primary') and contains(@class, 'button--block-level-mobile')]")))

                # Find the button and click on it
                ticket_button = driver.find_element(By.XPATH, "//a[contains(@class, 'button') and contains(@class, 'button--small') and contains(@class, 'button--primary') and contains(@class, 'button--block-level-mobile')]")
                time.sleep(self.spinbox.value())
                ticket_button.click()

                
                if driver.current_url == event_url:
                    pass
                else:
                    try:
                        wait.until(EC.element_to_be_clickable((By.ID, "choose-seat-button")))
                        seat_button= driver.find_element(By.ID, "choose-seat-button")
                        seat_button.click()
                        self.alert(self.whatsapp_number.text(), "Ticket Available. Hurry Up!")
                        break
                    except:
                        pass
            except:
                pass
            
            if self.stop_flag:
                break
     

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
