#global
import os
from unittest import skip
#django
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
#others app
from user.models import Profile
from products.models import Category, Product
#current app
from .utils import popdatabase, create_user_and_profile
print("test_us\n", "_ "*20)

class AccountTestCase(LiveServerTestCase):

    def test_user_stories(self):
        environment = os.environ["DJANGO_SETTINGS_MODULE"]
        production = "config.settings.production"
        travis = "config.settings.travis"
        print(environment, environment in (production,travis))
        if environment in (production,travis) : 
            print("on est pas en local ...")
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = True
            if environment == travis:
                print("car on est avec travis")
                self.driver = webdriver.Firefox(firefox_options=firefox_options)
            elif environment == production:
                print('car on est en prod')
                self.driver = webdriver.Firefox(firefox_options=firefox_options,executable_path="/home/blingstand/p10/env/bin/geckodriver")
            else:
                self.driver = webdriver.Firefox()
        self.user, self.profile = create_user_and_profile("test", "test")
        popdatabase()

        print("\n\n***\ndébut des test\n***")
        #Opening the link we want to test
        register = f"{self.live_server_url}/p10/user/register"
        self.driver.get(register)

        assert self.driver.current_url == register
        print("-- chargement page register ok")
        #find the form element
        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')
        #fill form and confirm
        username.send_keys('test1')
        password.send_keys('test')
        submit.send_keys(Keys.RETURN)
        #find th feedback element
        wait(self.driver, 10).until(lambda driver: driver.current_url != register)

        feedback = self.driver.find_element_by_id('id_feed_back_connexion')
        assert "Félicitation vous venez de créer : test1 !" == feedback.text
        print("> création nouvel utilisateur ok\n")

        connection = f"{self.live_server_url}/p10/user/connection"
        assert self.driver.current_url == connection
        print("-- chargement page connexion ok")

        username = self.driver.find_element_by_id('id_username')
        password = self.driver.find_element_by_id('id_password')
        submit = self.driver.find_element_by_id('id_submit')
        username.send_keys('test')
        password.send_keys('test')
        submit.send_keys(Keys.RETURN)
        index = f"{self.live_server_url}/p10/research/index"
        wait(self.driver, 10).until(lambda driver: driver.current_url != connection)
        print("> connexion du nouvel utilisateur ok\n")
        
        assert self.driver.current_url == index
        print("-- chargement page index ok")
        
        
        logo_my_account = self.driver.find_element_by_id("id_my_account_logo")
        logo_my_account.click()
        my_account = f"{self.live_server_url}/p10/user/myAccount"
        wait(self.driver, 10).until(lambda driver: driver.current_url != index)
        print("> click sur icône mon compte ok\n")

        assert self.driver.current_url == my_account
        print("-- chargement page myAccount ok")

        #NEED FOR A SOLUTION TO TEST MAIL SEND
        # mail = self.driver.find_element_by_id('id_mail')
        # submit = self.driver.find_element_by_id('id_submit')
        # mail.send_keys('mail@test.com')
        # submit.send_keys(Keys.RETURN)
        # mail_communicated = wait(self.driver, 5)\
        # .until(lambda driver: driver.find_element_by_id("id_mail_communicated"))
        # assert mail_communicated.text == "Tu m'as communiqué ce mail : mail@test.com"
        # print("> ajout du mail ok\n")

        mini_search = self.driver.find_element_by_id('nav-mini-search')
        mini_submit = self.driver.find_element_by_id('nav-mini-submit')
        mini_search.send_keys("test")
        mini_submit.send_keys(Keys.RETURN)
        wait(self.driver, 10).until(lambda driver: self.driver.current_url != my_account)

        assert self.driver.current_url == index
        print("-- chargement de la page index ok")

        index_msg_error = self.driver.find_element_by_id('index-msg-error')

        assert index_msg_error.text[:16] == "Pas de résultats"
        print("> pas de resultats pour la recherche 'test'\n")

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
        search1 = f"{self.live_server_url}/p10/research/results/jus%20de%20fruits/jus%20d'orange"
        
        assert self.driver.current_url == search1
        print("-- chargement de la page des résultats ok")

        add_favorite_button = self.driver.find_element_by_name("fav-Jus d'orange - Solevita - 1 L")
        add_favorite_button.click()

        wait(self.driver, 10).until(lambda driver: self.driver.current_url != search1)
        print("> ajout d'un produit au favoris\n")
        add_favorite = f"{self.live_server_url}/p10/user/favorite/Jus%20d'orange%20-%20Solevita%20-%201%20L"

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

        search2 = f"{self.live_server_url}/p10/user/favorite/Pur%20jus%20d'orange%20sans%20pulpe"
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


        favorite = f"{self.live_server_url}/p10/user/favorite"
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





    




