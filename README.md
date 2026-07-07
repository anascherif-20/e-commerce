# Lunéa Atelier — E-commerce de bracelets personnalisés

Application web e-commerce développée avec Flask pour la vente et la personnalisation de bracelets faits main. Projet réalisé dans le cadre d'un PFE (Projet de Fin d'Études).

## Fonctionnalités

- **Accueil** — présentation de la marque, collections et savoir-faire
- **Boutique** — catalogue de bracelets avec photos, catégories et filtres
- **Personnalisation** — création d'un bracelet sur mesure avec aperçu en temps réel (texte, couleur, taille, perles, prix)
- **Panier** — panier en session, quantités, bracelets personnalisés, commande via modal de paiement
- **Profil** — informations du client et historique complet de ses commandes
- **Connexion / Inscription** — authentification avec mots de passe hachés (Werkzeug)
- **Contact** — formulaire de contact

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | Python 3 / Flask |
| Base de données | MySQL (mysql-connector-python) |
| Templating | Jinja2 |
| Frontend | HTML5 / CSS3 « Liquid Glass » (`static/style.css`) + JavaScript vanilla |

## Structure du projet

```
e-commerce/
├── app.py                  # Application Flask — toutes les routes
├── database.py             # Connexion MySQL (variables d'environnement)
├── requirements.txt        # Dépendances Python
├── vercel.json             # Configuration de déploiement Vercel
├── schema.sql              # Schéma de la base + catalogue produits
├── static/
│   ├── style.css           # Styles globaux
│   └── images/             # Photos des produits
└── templates/
    ├── base.html           # Layout partagé (navbar + footer + JS commun)
    ├── accueil.html
    ├── boutique.html
    ├── personnalisation.html
    ├── panier.html
    ├── profil.html
    ├── connexion.html
    ├── inscription.html
    └── contact.html
```

## Lancer le projet en local

**Prérequis :** Python 3.10+ et MySQL 8.

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd e-commerce

# 2. Créer et activer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer la base de données
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ecommerce"
mysql -u root -p ecommerce < schema.sql

# 5. Démarrer le serveur
python app.py
```

L'application est accessible sur [http://localhost:5001](http://localhost:5001).

Par défaut la connexion locale utilise `root` / mot de passe `amine` sur la base
`ecommerce`. Pour utiliser d'autres identifiants, définissez `DB_USER`,
`DB_PASSWORD`, `DB_NAME`, `DB_HOST`, `DB_PORT` avant de lancer l'application.

## Déploiement sur Vercel (via GitHub)

Vercel exécute l'application en mode *serverless* mais **n'héberge pas de base
MySQL** : il faut d'abord une base MySQL cloud.

### 1. Créer la base MySQL cloud

Chez le fournisseur de votre choix (Railway, Aiven, PlanetScale, Clever Cloud,
filess.io — la plupart ont une offre gratuite) :

1. Créez une base MySQL et récupérez l'URL de connexion
   (`mysql://user:password@host:port/dbname`).
2. Importez le schéma et le catalogue :

```bash
mysql -h <host> -P <port> -u <user> -p <dbname> < schema.sql
```

### 2. Pousser le code sur GitHub

```bash
git add .
git commit -m "Prêt pour le déploiement Vercel"
git push origin main
```

### 3. Importer le projet dans Vercel

1. Sur [vercel.com](https://vercel.com), **Add New → Project** puis importez le
   dépôt GitHub.
2. Ne changez rien au build (le fichier `vercel.json` configure tout :
   `app.py` en fonction Python, `static/` servi par le CDN).
3. Dans **Settings → Environment Variables**, ajoutez :

| Variable | Valeur | Rôle |
|----------|--------|------|
| `SECRET_KEY` | une longue chaîne aléatoire | signe les sessions Flask |
| `DATABASE_URL` | `mysql://user:pass@host:port/dbname` | connexion à la base cloud |
| `DB_SSL_CA` *(si exigé)* | chemin du bundle CA, ex. `/etc/ssl/certs/ca-certificates.crt` | TLS vers la base |

   > Alternative à `DATABASE_URL` : définir séparément `DB_HOST`, `DB_PORT`,
   > `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

4. Cliquez sur **Deploy**. Chaque `git push` déclenchera ensuite un
   redéploiement automatique.

### Générer une SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Routes disponibles

| URL | Page |
|-----|------|
| `/` | Accueil |
| `/boutique` | Boutique (`?categorie=` pour filtrer) |
| `/personnalisation` | Personnalisation avec aperçu live |
| `/panier` | Panier et commande |
| `/profil` | Profil et historique des commandes |
| `/connexion` · `/inscription` · `/deconnexion` | Authentification |
| `/contact` | Contact |
