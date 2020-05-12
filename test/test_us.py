from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait

from user.models import Profile
from products.models import Category, Product

print("test_us\n", "_ "*20)

class AccountTestCase(LiveServerTestCase):

    def test_user_stories(self):
        print("\n\n***\ndébut des test\n***")
        #self.driver = webdriver.Firefox('/home/blingstand/Bureau/openclassrooms/projets/projet8/pureBeurre/')
        self.driver = webdriver.Firefox()
        self.user = User(username="test")
        self.user.set_password("123")
        self.user.save()
        self.category = Category(name="jus de fruits")
        self.category.save()
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore="b", packaging="osef")
        self.product2 = Product(
            name="Jus d'orange - Solevita - 1 L", 
            image_url="https://static.openfoodfacts.org/images/products/20245900/front_fr.148.full.jpg",
            url="https://fr.openfoodfacts.org/produit/20245900/jus-d-orange-solevita", 
            nutriscore="c", packaging="osef")
        self.product1.save()
        self.product2.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product1.save()
        self.product2.save()
        self.category2 = Category(name="compote")
        self.category2.save()
        self.product3 = Product(
            name="Pomme pur fruit pressé", 
            image_url="https://static.openfoodfacts.org/images/products/20376451/front_fr.136.full.jpg",
            url="https://fr.openfoodfacts.org/produit/20376451/pomme-pur-fruit-presse-solevita", 
            nutriscore="c", packaging="osef")
        self.product4 = Product(
            name="Pom'Potes pomme", 
            image_url="https://static.openfoodfacts.org/images/products/10217603/front_fr.64.full.jpg",
            url="https://fr.openfoodfacts.org/produit/10217603/pom-potes-pomme", 
            nutriscore="c", packaging="osef")
        self.product3.save()
        self.product4.save()
        self.product3.category.add(self.category)
        self.product4.category.add(self.category2)
        self.product3.save()
        self.product4.save()
        #Opening the link we want to test
        register = f"{self.live_server_url}/user/register"
        self.driver.get(register)

        assert self.driver.current_url == register
        print("-- chargement page register ok")
        #find the form element
        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')
        #fill form and confirm
        username.send_keys('test1')
        password.send_keys('123')
        submit.send_keys(Keys.RETURN)
        #find th feedback element
        wait(self.driver, 10).until(lambda driver: driver.current_url != register)

        feedback = self.driver.find_element_by_id('id_feed_back_connexion')
        assert "Félicitation vous venez de créer : test1 !" == feedback.text
        print("> création nouvel utilisateur ok\n")

        connection = f"{self.live_server_url}/user/connection"
        assert self.driver.current_url == connection
        print("-- chargement page connexion ok")

        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')
        username.send_keys('test')
        password.send_keys('123')
        submit.send_keys(Keys.RETURN)
        index = f"{self.live_server_url}/research/index"
        wait(self.driver, 10).until(lambda driver: driver.current_url != connection)
        print("> connexion du nouvel utilisateur ok\n")
        
        assert self.driver.current_url == index
        print("-- chargement page index ok")
        
        self.profile = Profile(user=self.user)
        self.profile.save()
        logo_my_account = self.driver.find_element_by_id("id_my_account_logo")
        logo_my_account.click()
        my_account = f"{self.live_server_url}/user/myAccount"
        wait(self.driver, 10).until(lambda driver: driver.current_url != index)
        print("> click sur icône mon compte ok\n")

        assert self.driver.current_url == my_account
        print("-- chargement page myAccount ok")


        mail = self.driver.find_element_by_id('id_mail')
        submit = self.driver.find_element_by_id('id_submit')
        mail.send_keys('mail@test.com')
        submit.send_keys(Keys.RETURN)
        mail_communicated = wait(self.driver, 5)\
        .until(lambda driver: driver.find_element_by_id("id_mail_communicated"))
        assert mail_communicated.text == "Tu m'as communiqué ce mail : mail@test.com"
        print("> ajout du mail ok\n")

        mini_search = self.driver.find_element_by_id('nav-mini-search')
        mini_submit = self.driver.find_element_by_id('nav-mini-submit')
        mini_search.send_keys("123")
        mini_submit.send_keys(Keys.RETURN)
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != my_account)

        assert self.driver.current_url == index
        print("-- chargement de la page index ok")

        index_msg_error = self.driver.find_element_by_id('index-msg-error')

        assert index_msg_error.text[:16] == "Pas de résultats"
        print("> pas de resultats pour la recherche '123'\n")

        assert self.driver.current_url == index
        print("-- toujours sur la page index")
        search = self.driver.find_element_by_id('simple-form-input')
        submit = self.driver.find_element_by_id('simple-form-submit')
        search.send_keys("jus d'orange")
        print("> nouvelle recherche : jus d'orange ok")
        submit.send_keys(Keys.RETURN)
        category = wait(self.driver, 3).until(lambda driver: \
            self.driver.find_element_by_id("index-cat-jusdefruits"))
        print(f"> resultat : catégorie '{category.text}'.")

        category.click()
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != index)
        print("> je clique sur le bouton jus de fruit.\n")
        search1 = f"{self.live_server_url}/research/results/jus%20de%20fruits/jus%20d'orange"
        
        assert self.driver.current_url == search1
        print("-- chargement de la page des résultats ok")

        add_favorite_button = self.driver.find_element_by_name("fav-Jus d'orange - Solevita - 1 L")
        add_favorite_button.click()

        wait(self.driver, 10).until(lambda driver: self.driver.current_url != search1)
        print("> ajout d'un produit au favoris\n")
        add_favorite = f"{self.live_server_url}/user/favorite/Jus%20d'orange%20-%20Solevita%20-%201%20L"

        assert self.driver.current_url == add_favorite
        print("-- chargement de la page favoris")

        favorites = self.driver.find_elements_by_class_name("cont-img-result")
        print(f"==> Il y a {len(favorites)} produit(s) ajouté(s) aux favoris")

        mini_search = self.driver.find_element_by_id('nav-mini-search')
        mini_submit = self.driver.find_element_by_id('nav-mini-submit')
        mini_search.send_keys("Pur jus d'orange sans pulpe")
        mini_submit.send_keys(Keys.RETURN)
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != add_favorite)
        print("> nouvelle recherche : Pur jus d'orange sans pulpe ok\n")

        assert self.driver.current_url == index
        print("-- chargement de la page results ok ")

        add_favorite_button2 = self.driver.find_element_by_name("fav-Pur jus d'orange sans pulpe")
        add_favorite_button2.click()
        print("> ajout d'un produit au favoris ok \n")

        search2 = f"{self.live_server_url}/user/favorite/Pur%20jus%20d'orange%20sans%20pulpe"
        assert self.driver.current_url == search2
        favorites = self.driver.find_elements_by_class_name("cont-img-result")
        print(f"==> Il y a {len(favorites)} produit(s) ajouté(s) aux favoris")

        biscuit = self.driver.find_element_by_id("biscuit")
        biscuit.click()
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != add_favorite)
        
        assert self.driver.current_url == index
        print("-- chargement de la page index ok ")

        carrot_icone = self.driver.find_element_by_id('id_carrot')
        carrot_icone.click()
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != index)
        print("> click sur l'icône carrote\n")


        favorite = f"{self.live_server_url}/user/favorite"
        assert self.driver.current_url == favorite
        print("-- chargement de la page favoris ok ")

        assert len(favorites) == 2
        print(f"==> Il y a {len(favorites)} produit(s) dans les favoris")

        disco = self.driver.find_element_by_id("id_disconnect")
        disco.click()
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != favorite)
        print("> click sur l'icône deconnexion\n")

        assert self.driver.current_url == index
        print("-- chargement de la page index")

        self.driver.quit()
        print("\n\n***\nfin des test\n***")





    






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
