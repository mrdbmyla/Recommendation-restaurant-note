# 🍝 Projet Prédiction de note restaurant

## 📌 Contexte

Ce projet part d’une idée simple : utiliser le **Machine Learning** pour aider à anticiper la note d’un restaurant en fonction de critères comme l’emplacement, le type de cuisine ou d’autres facteurs clés.

L’intérêt stratégique est de transformer des données en outil d’aide à la décision. Plutôt que de se baser uniquement sur l’intuition, l’utilisateur peut tester différents scénarios et voir ce qui influence réellement la perception des clients.

Cela permet :

- de réduire le risque avant d’ouvrir un restaurant
- d’optimiser son positionnement (lieu, type, offre)
- de mieux comprendre les facteurs de succès

**L’objectif n’est pas seulement de prédire une note, mais d’offrir un outil interactif pour explorer et prendre de meilleures décisions.**

## 🧩 Objectifs & Enjeux

1. Maîtriser les techniques de collecte de données à partir de différentes sources (APIs, fichiers, bases de données).
2. Développer des compétences en prétraitement et nettoyage de données avec Python.
3. Concevoir et implémenter un pipeline ETL.
4. Gérer efficacement une base de données relationnelle.
5. Créer des visualisations interactives et des tableaux de bord dynamiques.
6. Explorer les possibilités d’enrichissement par l’intelligence artificielle.

**J’ai utilisé différentes APIs pour enrichir les données :**

- Une API météo pour analyser si la présence d’une terrasse peut avoir un impact positif sur la note du restaurant
- Une API permettant d’estimer le revenu médian selon les États, étant donné que les prédictions concernent des adresses situées aux États-Unis

J’ai également mis en place un pipeline de données automatisé avec **Apache Airflow**, qui permet de mettre à jour les données quotidiennement (notamment les APIs) afin de garantir des informations toujours actuelles.

## Dashboards KPI

![dashboard_bi1](images/bi1.png)
![dashboard_bi2](images/bi2.png)

## 🛠️ Outils Utilisés  
- **Base de données** : Kaggle
- **Langage** : DAX
- **Visualisation** : Power BI

## ⭐ Projet réalisé par :
- Mourad B.
