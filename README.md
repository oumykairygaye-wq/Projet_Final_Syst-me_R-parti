Système Distribué de Supervision des noeuds d'un réseau

1. Présentation du projet

Ce projet a été réalisé dans le cadre du module Systèmes Répartis en Master 1 Réseaux et Infrastructures Virtuelles.

L’objectif du projet est de développer un système distribué de supervision des noeuds d'un réseau.

Le système repose sur une architecture client–serveur:

* Les clients (agents) collectent les métriques système.
* Le serveur central reçoit les données, les affiche et les enregistre.

Les informations collectées permettent de surveiller l’état des machines d’un réseau.


2. Architecture du système

Le système est composé de deux éléments principaux :

* Agent client

Le client collecte les informations système et les envoie périodiquement au serveur.

* Serveur de supervision

Le serveur reçoit les métriques envoyées par les clients, les affiche dans le terminal et les enregistre dans une base de données.

Plusieurs clients peuvent se connecter au serveur simultanément.


3. Structure du projet


distributed-monitoring-system
│
├── client
│   └── client.py
│
├── server
│   └── server.py
│
├── config
│   └── config.py
│
├── logs
│
├── database
│
└── README.md



4. Explication du fonctionnement du code

4.1 Le client (client.py)

Le programme client agit comme un agent de supervision.

Il réalise plusieurs tâches :

* Collecte des métriques système

Le client utilise la bibliothèque psutil pour collecter :

* utilisation du CPU
* utilisation de la mémoire
* temps de fonctionnement du système (uptime)
* Vérification des ports
Certains ports réseau sont vérifiés afin de savoir s’ils sont ouverts ou fermés 
* Vérification des services
Le client vérifie également si certains services ou processus sont actifs sur la machine.


Les métriques collectées sont :

1. converties au format JSON
2. envoyées au serveur via une connexion TCP

Les données sont envoyées toutes les 5 secondes.



4.2 Le serveur (server.py)

Le serveur est le composant central du système.

* Réception des connexions

Le serveur ouvre un socket TCP et attend les connexions des clients.

* Gestion de plusieurs clients

Pour permettre à plusieurs clients de se connecter en même temps, le serveur utilise le multi-threading.

Chaque client est traité dans un thread indépendant.

* Traitement des métriques

Lorsque le serveur reçoit un message :

* il décode le message JSON
* il extrait les métriques
* il affiche les informations dans le terminal

* Enregistrement des données

Les métriques reçues sont enregistrées dans une **base de données SQLite** afin de conserver un historique.

* Système d’alerte

Le serveur peut générer une alerte si :

* l’utilisation du CPU dépasse 90%.



5 Technologies utilisées

Les technologies utilisées dans ce projet sont :

* Python
* Sockets TCP
* JSON
* SQLite
* Multi-threading
* Logging
* Bibliothèque **psutil**



5 Environnement de développement

Le projet a été développé en utilisant :

* Visual Studio Code comme environnement de développement
* Python pour l’implémentation du système distribué



6 Choix techniques

Plusieurs choix techniques ont été réalisés lors du développement du projet.

Le langage Python a été choisi pour sa simplicité et sa capacité à développer rapidement des applications réseau.

La communication entre le client et le serveur utilise les sockets TCP, ce qui garantit une transmission fiable des données.

Le format JSON a été utilisé pour structurer les données échangées entre le client et le serveur.

La bibliothèque psutil permet de récupérer facilement les métriques système.

Pour le stockage des données, SQLite a été choisi car il s’agit d’une base de données légère qui ne nécessite pas de serveur externe.

Le projet a été développé avec Visual Studio Code, ce qui a facilité l’organisation du code et le débogage du programme.



7 Difficultés rencontrées

Durant la réalisation du projet, certaines difficultés ont été rencontrées.

La première difficulté concernait la **communication entre le client et le serveur**. Au début, les métriques envoyées par le client n’étaient pas correctement affichées sur le serveur.

Une autre difficulté était la **gestion de plusieurs clients simultanément**, ce qui a nécessité l’utilisation du multi-threading.

La compréhension et l’utilisation de la bibliothèque **psutil** ont également demandé un certain temps d’apprentissage.

Enfin, il a fallu organiser correctement la **structure du projet** afin de rendre le code plus clair et plus facile à maintenir.



8 Exécution du projet

* Lancer le serveur

python server/server.py avec la commande suivante: python -m server.server 


* Lancer le client

python client/client.py avec la commande suivante : python -m client.client


Le client envoie automatiquement les métriques au serveur toutes les 5 secondes.



9 Améliorations possibles

Dans une version future du projet, plusieurs améliorations pourraient être envisagées :

* création d’une interface web de supervision
* visualisation des métriques 
* système d’alertes plus avancé
* déploiement du système sur plusieurs machines dans un environnement réel.


# Auteur

Oumy Kairy Gaye

Master 1 – Réseaux et Infrastructures Virtuelles
