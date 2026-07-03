import os
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

app = Flask(__name__)

# Set SECRET_KEY via environment variable in production; fallback only for local dev.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/boutique")
def boutique():
    categorie = request.args.get("categorie")
    db, cursor = get_db()
    try:
        if categorie:
            cursor.execute("SELECT * FROM produits WHERE categorie = %s", (categorie,))
        else:
            cursor.execute("SELECT * FROM produits")
        produits = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template("boutique.html", produits=produits, categorie=categorie)


@app.route("/personnalisation")
def personnalisation():
    return render_template("personnalisation.html")


@app.route("/panier")
def panier():
    if "utilisateur_id" not in session:
        return redirect("/connexion")

    panier_session = session.get("panier", {})
    articles = []
    total = 0.0

    if panier_session:
        # Extract unique integer product IDs from the keys
        produit_ids = set()
        for key in panier_session.keys():
            parts = key.split("_")
            produit_ids.add(int(parts[0]))

        db, cursor = get_db()
        try:
            placeholders = ",".join(["%s"] * len(produit_ids))
            cursor.execute(f"SELECT * FROM produits WHERE id IN ({placeholders})", list(produit_ids))
            produits_db = cursor.fetchall()
        finally:
            cursor.close()
            db.close()

        produits_map = {p["id"]: p for p in produits_db}

        for key, quantite in panier_session.items():
            parts = key.split("_")
            produit_id = int(parts[0])
            produit = produits_map.get(produit_id)
            if not produit:
                continue

            is_custom = len(parts) > 1 and parts[1] == "custom"
            custom_details = None
            if is_custom:
                custom_details = {
                    "texte": parts[2],
                    "couleur": parts[3],
                    "taille": parts[4],
                    "type_perles": parts[5]
                }

            sous_total = float(produit["prix"]) * quantite
            total += sous_total
            articles.append({
                "key": key,
                "produit": produit,
                "quantite": quantite,
                "sous_total": sous_total,
                "is_custom": is_custom,
                "custom_details": custom_details
            })

    return render_template("panier.html", articles=articles, total=total)


@app.route("/panier/modifier/<key>", methods=["POST"])
def modifier_quantite(key):
    if "utilisateur_id" not in session:
        return redirect("/connexion")
    action = request.form.get("action")
    panier = session.get("panier", {})
    if key in panier:
        if action == "incrementer":
            panier[key] = panier[key] + 1
        elif action == "decrementer":
            panier[key] = panier[key] - 1
            if panier[key] <= 0:
                panier.pop(key, None)
    session["panier"] = panier
    session.modified = True
    return redirect("/panier")


@app.route("/panier/supprimer/<key>", methods=["POST"])
def supprimer_du_panier(key):
    if "utilisateur_id" not in session:
        return redirect("/connexion")
    panier = session.get("panier", {})
    panier.pop(key, None)
    session["panier"] = panier
    session.modified = True
    flash("Article retiré du panier.", "success")
    return redirect("/panier")


@app.route("/personnalisation/ajouter", methods=["POST"])
def ajouter_custom_panier():
    if "utilisateur_id" not in session:
        flash("Connectez-vous pour ajouter des articles au panier.", "error")
        return redirect("/connexion")

    texte = request.form.get("texte", "").strip()
    if not texte:
        texte = "LINA"  # Default fallback if empty
    couleur = request.form.get("couleur", "Rose poudré")
    taille = request.form.get("taille", "Adulte")
    type_perles = request.form.get("type_perles", "Perles moyennes")
    try:
        quantite = int(request.form.get("quantite", 1))
        if quantite < 1:
            quantite = 1
    except ValueError:
        quantite = 1

    # Product ID for the base customizable bracelet is 1 (Bracelet Luna, 19.99 €)
    produit_id = 1
    key = f"{produit_id}_custom_{texte}_{couleur}_{taille}_{type_perles}"

    panier = session.get("panier", {})
    panier[key] = panier.get(key, 0) + quantite
    session["panier"] = panier
    session.modified = True

    flash("Bracelet personnalisé ajouté au panier !", "success")
    return redirect("/panier")


@app.route("/commander", methods=["POST"])
def commander():
    if "utilisateur_id" not in session:
        return redirect("/connexion")

    panier_session = session.get("panier", {})
    if not panier_session:
        flash("Votre panier est vide.", "error")
        return redirect("/boutique")

    produit_ids = set()
    for key in panier_session.keys():
        parts = key.split("_")
        produit_ids.add(int(parts[0]))

    db, cursor = get_db()
    try:
        placeholders = ",".join(["%s"] * len(produit_ids))
        cursor.execute(f"SELECT * FROM produits WHERE id IN ({placeholders})", list(produit_ids))
        produits_db = cursor.fetchall()
        produits_map = {p["id"]: p for p in produits_db}

        total = 0.0
        order_items = []
        for key, quantite in panier_session.items():
            parts = key.split("_")
            produit_id = int(parts[0])
            produit = produits_map.get(produit_id)
            if not produit:
                continue

            is_custom = len(parts) > 1 and parts[1] == "custom"
            custom_details = None
            if is_custom:
                custom_details = {
                    "texte": parts[2],
                    "couleur": parts[3],
                    "taille": parts[4],
                    "type_perles": parts[5]
                }

            prix = float(produit["prix"])
            total += prix * quantite
            order_items.append({
                "produit_id": produit_id,
                "quantite": quantite,
                "prix_unitaire": prix,
                "is_custom": is_custom,
                "custom_details": custom_details
            })

        # Save address and details in flash/simulation log, or users table telephone update
        telephone = request.form.get("telephone", "")
        if telephone:
            cursor.execute(
                "UPDATE utilisateurs SET telephone = %s WHERE id = %s",
                (telephone, session["utilisateur_id"])
            )

        # Create Order record
        utilisateur_id = session["utilisateur_id"]
        cursor.execute(
            "INSERT INTO commandes (utilisateur_id, montant_total, statut) VALUES (%s, %s, %s)",
            (utilisateur_id, total, "En attente")
        )
        commande_id = cursor.lastrowid

        # Create Order Items and Customizations records
        for item in order_items:
            cursor.execute(
                "INSERT INTO details_commande (commande_id, produit_id, quantite, prix_unitaire) VALUES (%s, %s, %s, %s)",
                (commande_id, item["produit_id"], item["quantite"], item["prix_unitaire"])
            )
            detail_id = cursor.lastrowid

            if item["is_custom"]:
                det = item["custom_details"]
                cursor.execute(
                    "INSERT INTO personnalisations (detail_commande_id, texte, couleur, taille, type_perles) VALUES (%s, %s, %s, %s, %s)",
                    (detail_id, det["texte"], det["couleur"], det["taille"], det["type_perles"])
                )

        db.commit()
        session.pop("panier", None)
        flash("Votre commande a été validée avec succès ! Merci de votre confiance.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Une erreur est survenue lors de la commande : {str(e)}", "error")
    finally:
        cursor.close()
        db.close()

    return redirect("/panier")


MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin",
           "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def date_francaise(d):
    """Format a datetime as '3 juillet 2026'."""
    if not d:
        return ""
    return f"{d.day} {MOIS_FR[d.month - 1]} {d.year}"


@app.route("/profil")
def profil():
    if "utilisateur_id" not in session:
        flash("Connectez-vous pour accéder à votre profil.", "error")
        return redirect("/connexion")

    utilisateur_id = session["utilisateur_id"]
    db, cursor = get_db()
    try:
        cursor.execute(
            "SELECT id, nom, prenom, email, telephone, date_inscription FROM utilisateurs WHERE id = %s",
            (utilisateur_id,),
        )
        utilisateur = cursor.fetchone()
        if not utilisateur:
            session.clear()
            return redirect("/connexion")

        cursor.execute(
            "SELECT * FROM commandes WHERE utilisateur_id = %s ORDER BY date_commande DESC, id DESC",
            (utilisateur_id,),
        )
        commandes = cursor.fetchall()

        details_par_commande = {}
        if commandes:
            ids = [c["id"] for c in commandes]
            placeholders = ",".join(["%s"] * len(ids))
            cursor.execute(
                f"""
                SELECT dc.commande_id, dc.quantite, dc.prix_unitaire,
                       p.nom AS produit_nom, p.image AS produit_image, p.categorie AS produit_categorie,
                       pe.texte AS perso_texte, pe.couleur AS perso_couleur,
                       pe.taille AS perso_taille, pe.type_perles AS perso_perles
                FROM details_commande dc
                JOIN produits p ON p.id = dc.produit_id
                LEFT JOIN personnalisations pe ON pe.detail_commande_id = dc.id
                WHERE dc.commande_id IN ({placeholders})
                ORDER BY dc.id
                """,
                ids,
            )
            for row in cursor.fetchall():
                details_par_commande.setdefault(row["commande_id"], []).append(row)
    finally:
        cursor.close()
        db.close()

    for commande in commandes:
        commande["articles"] = details_par_commande.get(commande["id"], [])
        commande["nb_articles"] = sum(a["quantite"] for a in commande["articles"])
        commande["date_affichee"] = date_francaise(commande.get("date_commande"))

    total_depense = sum(float(c["montant_total"]) for c in commandes)
    total_articles = sum(c["nb_articles"] for c in commandes)

    return render_template(
        "profil.html",
        utilisateur=utilisateur,
        commandes=commandes,
        total_depense=total_depense,
        total_articles=total_articles,
        membre_depuis=date_francaise(utilisateur.get("date_inscription")),
    )


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]

        db, cursor = get_db()
        try:
            cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
            utilisateur = cursor.fetchone()
        finally:
            cursor.close()
            db.close()

        if utilisateur and check_password_hash(utilisateur["mot_de_passe"], mot_de_passe):
            session["utilisateur_id"] = utilisateur["id"]
            session["prenom"] = utilisateur["prenom"]
            flash(f"Bienvenue, {utilisateur['prenom']} !", "success")
            return redirect("/")

        return render_template("connexion.html", erreur="Email ou mot de passe incorrect.")

    return render_template("connexion.html")


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = generate_password_hash(request.form["mot_de_passe"])

        db, cursor = get_db()
        try:
            cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)",
                (nom, prenom, email, mot_de_passe),
            )
            db.commit()
        except Exception:
            return render_template("inscription.html", erreur="Cette adresse email est déjà utilisée.")
        finally:
            cursor.close()
            db.close()

        flash("Compte créé avec succès ! Connectez-vous.", "success")
        return redirect("/connexion")

    return render_template("inscription.html")


@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/ajouter/<int:produit_id>", methods=["POST"])
def ajouter_au_panier(produit_id):
    if "utilisateur_id" not in session:
        flash("Connectez-vous pour ajouter des articles au panier.", "error")
        return redirect("/connexion")

    db, cursor = get_db()
    try:
        cursor.execute("SELECT nom FROM produits WHERE id = %s", (produit_id,))
        produit = cursor.fetchone()
    finally:
        cursor.close()
        db.close()

    panier = session.get("panier", {})
    panier[str(produit_id)] = panier.get(str(produit_id), 0) + 1
    session["panier"] = panier
    session.modified = True

    nom = produit["nom"] if produit else "Produit"
    flash(f"« {nom} » ajouté au panier !", "success")
    return redirect("/boutique")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
