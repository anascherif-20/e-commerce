# Lunéa Atelier — E-commerce de bracelets personnalisés

Application web e-commerce développée avec Flask pour la vente et la personnalisation de bracelets faits main. Projet réalisé dans le cadre d'un PFE (Projet de Fin d'Études).

## Fonctionnalités

- **Accueil** — présentation de la marque et accès rapide à la boutique
- **Boutique** — catalogue de bracelets (Luna, Élégance, Auréa) avec catégories et prix
- **Personnalisation** — page dédiée à la création d'un bracelet sur mesure
- **Panier** — récapitulatif des articles sélectionnés avec calcul du total et frais de livraison
- **Connexion** — page d'authentification client
- **Contact** — formulaire de contact

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | Python 3 / Flask |
| Templating | Jinja2 |
| Frontend | HTML5 / CSS3 (feuille de style unique `style.css`) |

## Structure du projet

```
e-commerce/
├── app.py                  # Application Flask — routes principales
├── static/
│   └── style.css           # Styles globaux
└── templates/
    ├── base.html           # Layout partagé (navbar + footer)
    ├── accueil.html        # Page d'accueil
    ├── boutique.html       # Catalogue produits
    ├── personnalisation.html
    ├── panier.html         # Panier d'achat
    ├── connexion.html      # Authentification
    └── contact.html        # Contact
```

## Lancer le projet en local

**Prérequis :** Python 3.8+

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd e-commerce

# 2. Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install flask

# 4. Démarrer le serveur
python app.py
```

L'application est accessible sur [http://localhost:5001](http://localhost:5001).

## Routes disponibles

| URL | Page |
|-----|------|
| `/` | Accueil |
| `/boutique` | Boutique |
| `/personnalisation` | Personnalisation |
| `/panier` | Panier |
| `/connexion` | Connexion |
| `/contact` | Contact |
