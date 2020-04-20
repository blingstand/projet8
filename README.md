# Projet 8 : Openclassrooms 
*********************

Ce projet a été créé pour répondre aux exigence du projet 8 de la formation Openclassroom parcours Python. Il s'agit de créer un site web pour recherche un substitut aux produit du quotidien. [Mon site(https://blingpurebeurre.herokuapp.com/)]
Sur ce site vous pouvez actuellement : 
* vous inscrire,
* vous connecter/déconnecter,
* faire une recherche simple,
* ajouter un produit dans vos favoris, 
* renseigner un mail
* vous renseigner sur un produit


Développé avec Python 3.8, Django 3.0.3

# Table des matières
(utilisateur)
1. [Installation](#installation(linux))
2. [Configuration](#configuration)
3. [Utilisation du site](#utilisation)
(développers)
4. [Utilisation des Commandes](#commandes)
5. [Tests](#tests)

## Installation(linux)

Ouvrez le terminal puis tapez
    
    $ mkdir new_file
    $ cd new_file
    $ git init
    $ git clone https://github.com/blingstand/projet8.git
    $ virtualenv env -p votre_version_de_python
    $ source votre_version_de_python/bin/activate
    $ pip install -r requirements.txt

## Configuration

Dans mon projet vous allez avoir besoin d'un super utilisateur. Pour l'exemple je vais créer un 
compte admin/admin@mail.fr/mdpadmin (pseudo/mail/mot de passe).

Pour ce faire : 

        $ python manage.py createsuperuser
        Username: admin # pseudo souhaité et appuyez sur retour.
        Email address: admin@mail.fr # mail souhaité et appuyez sur retour
        Password: ******** # mot de passe souhaité et appuyez sur retour
        Password (again) : ******** # même mot de passe pour confirmer et appuyez sur retour
        Superuser created successfully. # preuve que tout va bien =)


## Utilisation

Je suppose que vous avez installé et configuré mon projet. Vous pouvez désormais le lancer en faisant : 

    $ python manage.py runserver

le système répondra : 

    System check identified no issues (0 silenced).
    March 20, 2020 - 11:17:10 #ma date de rédaction du readme =) 
    Django version 3.0.3, using settings 'pureBeurre.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Rendez-vous à cette adresse pour utiliser le site en local : http://127.0.0.1:8000/
Certaines fonctionnalités du site nécessitent de vous connecter, je vous incite à le faire dès le début à cette adresse après avoir créer un compte à cette adresse : http://127.0.0.1:8000/user/register.html

Je vous laisse ensuite explorer les fonctionnalités ...

************************************************
## Commandes

Pour ce qui est des commandes accessibles, tapez : 
    
    $ python manage.py -h #ouvre le helpeur

Dans cet extrait, vous trouverez les trois commandes que j'ai créé pour peupler mes tables Category et Product mais aussi pour les vider.
    
    [products]
    cat #permet de montrer, ajouter ou supprimer une catégorie (et ses produits)
    dropcp #vide les tables
    popcp #peuple les tables

Leur code est disponible [ici](https://github.com/blingstand/projet8/tree/master/products/management/commands).

Un exemple : 

    $ python manage.py dropcp
     * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
     Cette commande vide les tables Category et Product.
     avant : 
     cat / prod >  20  /  100
     après : 
     cat / prod >  0  /  0
     * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  

    $ python manage.py popcp 
     * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
    Cette commande peuple les tables Category et Product de la base.
    Astuce : Tapez python manage.py popcp -h pour découvrir les arguments 
    que vous pouvez passer à cette commande
    J'utilise la valeur par défaut de 5 produits/categorie
    mais cette valeur peut être changée avec python manage.py popcp --snp <int>
     *** Récupération des données depuis le site Open Food Fact ***
     *** Insertion des données dans la base ***
     * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  




## Tests

J'ai organisé mes tests de la manière suivante. Ils sont tous regroupés dans le dossier [test](https://github.com/blingstand/projet8/tree/master/test). Vous trouverez à l'intérieur un test pour chaque application. Au debut du testxxx.py vous aurez les tests unitaires et ensuite les tests d'intégrations. Seuls les tests de validation se trouvent séparés car j'ai jugé qu'ils n'appartenait non pas à une seule mais à toutes les applications.

Remarque : django-nose est installé sur ce projet ce qui signifie que le niveau de couverture des tests sera consultable. J'ai volontairement laissé le dossier .coverage pour mon correcteur Openclassrooms. 

Pour lancer les tests, c'est très simple tapez : 

    $ python manage.py test #lance tous les tests (codés pour le moment)
    $ python manage.py test test.test_user #lance que les tests de l'app user  (codés pour le moment)