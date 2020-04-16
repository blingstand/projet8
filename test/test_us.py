from django.test import LiveServerTestCase
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        #adress:http://127.0.0.1:8000/user/register
        driver = self.driver
        #Opening the link we want to test
        first_url = f"{self.live_server_url}/user/register"
        driver.get(first_url)
        #find the form element
        username = driver.find_element_by_id('id_username')
        password = driver.find_element_by_id('id_password')
        submit = driver.find_element_by_id('id_submit')
        #fill form and confirm
        username.send_keys('test1')
        password.send_keys('123')
        submit.send_keys(Keys.RETURN)

        #find th feedback element
        element = wait(driver, 10).until(lambda driver: driver.current_url != first_url)

        feedback = driver.find_element_by_id('id_feed_back_connexion')
        self.assertTrue("Félicitation vous venez de créer : test1 !" == feedback.text)

    # def get_el(self, selector):
    #   """ select an element"""
    #   return self.driver.find_element_by_css_selector(selector)

    # def open_page(self):
    #   """ open a page and return an input and a button"""
    #   self.driver.get("http://127.0.0.1:5000/")
    #   my_button = self.get_el("button")
    #   my_input = self.get_el("#myInput")
    #   return my_input, my_button

    # def first_caracters(self, text, size):
    #   """ reduce the size of a text"""
    #   to_return = ""
    #   if len(text) > size:
    #       for carac in text:
    #           to_return += carac
    #           if len(to_return) == size:
    #               return to_return
    #   return text

    # def starter(self, question, elem_to_wait):
    #   my_input, my_button = self.open_page()
    #   start_question = question
    #   my_input.send_keys(start_question)
    #   my_button.click()
    #   wait = ui.WebDriverWait(self.driver, 1000)
    #   wait.until(lambda driver: self.driver.find_element_by_css_selector(\
    #    elem_to_wait).is_displayed())
    #   return my_input, my_button

    # #1
    # def test_server_is_up_and_running(self):
    #   response = requests.get(self.get_server_url())
    #   self.assertEqual(response.status_code, 200)

    # # -------- test user stories
    # #2
    # def test_presence_input(self):
    #   """tests the presence of the #myInput element"""
    #   my_input = self.open_page()[0]
    #   assert my_input is not None

    # #3
    # def test_presence_button(self):
    #   """tests the presence of the class .button element"""
    #   my_button = self.open_page()[1]
    #   assert my_button is not None

    # #4
    # def test_ask_something(self):
    #   """test wether the question is displayed"""
    #   start_question = "Où se trouve Bordeaux ?"
    #   self.starter(question=start_question,\
    #    elem_to_wait=".chatSelf .chat-message")
        
    #   chat_message = self.get_el(".chatSelf .chat-message")
    #   text_question = chat_message.text
    #   assert text_question == start_question

    # #5
    # def test_error_message(self):
    #   """ test wether error msg works """
    #   self.starter("", elem_to_wait=".rep-chat-message")

    #   chat_message = self.get_el(".rep-chat-message")
    #   response_text = chat_message.text
    #   assert response_text[0:6] == "Désolé"

    # #6
    # def test_get_response(self):
    #   """In case of answer test whether everything is good"""
    #   my_input, my_button = self.starter("Où se trouve Bordeaux ?",".rep-chat-message")

    #   chat_message = self.get_el(".rep-chat-message p:first-child")
    #   answer1 = chat_message.text
    #   answer1 = self.first_caracters(answer1, 32)
    #   chat_message = self.get_el(".rep-chat-message p:nth-child(2)")
    #   if chat_message is not None:
    #       answer2 = True
    #   chat_message = self.get_el(".rep-chat-message p:nth-child(3)")
    #   answer3 = chat_message.text
    #   answer3 = self.first_caracters(answer3, 8)
    #   expected_answer = ["Laisse-moi t'en parler un peu :)", True, "Bordeaux"]
    #   received_answer = [answer1, answer2, answer3]
    #   self.driver.quit()
    #   assert expected_answer == received_answer
