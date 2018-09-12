import unittest, time, random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewTest(unittest.TestCase):

# variables
    mail = 'test_sele@mail.ru'
    mail2 = 'test_sele2@mail.ru'
    password = 'aq1sw2de3'
    site = "https://mail.ru"
    check_number = random.randint(1000, 10000)

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:\Examples3\chromedriver')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_sending_the_mail(self):

        driver = self.driver
        driver.get(self.site)
        
# log-in first account
        login_field = driver.find_element_by_id("mailbox:login")
        login_field.click()
        login_field.send_keys(self.mail)
        password_field = driver.find_element_by_id("mailbox:password")
        password_field.send_keys(self.password)
        button_login = driver.find_element_by_id("mailbox:submit")
        button_login.click()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, 'PH_user-email'),
                                                 self.mail)
            )
        finally:
            userMail = driver.find_element_by_id("PH_user-email")

        assert userMail.text ==self.mail
# sending the mail
        button = driver.find_element(By.XPATH, "//*[@class='b-toolbar__btn__text b-toolbar__btn__text_pad']")
        button.click()

        actions = ActionChains(self.driver)
        actions.send_keys(self.mail2)
        actions.perform()

        the_theme = driver.find_element(By.XPATH, "//*[@tabindex='7']")
        the_theme.send_keys('Test')

        iframe = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)
        Text = driver.find_element(By.ID, "tinymce")
        Text.send_keys('This is test mail. The check number is ' + str(self.check_number))

        driver.switch_to.default_content()
        driver.find_element(By.XPATH, "//span[@class='b-toolbar__btn__text']").click()
        driver.find_element(By.ID, 'PH_logoutLink').click()
        
# log-in second account
        login_field = driver.find_element_by_id("mailbox:login")
        login_field.clear()
        login_field.send_keys(self.mail2)
        password_field = driver.find_element_by_id("mailbox:password")
        password_field.send_keys(self.password)
        button_login = driver.find_element_by_id("mailbox:submit")
        button_login.click()
        new_mail = driver.find_element(By.XPATH, "//div[@data-bem='b-datalist__item']")
        new_mail.click()
        read_new = driver.find_element(By.XPATH, "//*[@class = 'js-helper js-readmsg-msg'][1][1]")
        
# check the control number
        length_1 = len('This is test mail. The check number is ' + str(self.check_number))
        newline = read_new.text[:length_1]
        assert newline == 'This is test mail. The check number is ' + str(self.check_number)

    def tear_down(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
