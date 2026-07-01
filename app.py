import os
from flask import Flask, render_template, request, redirect, session
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

    return render_template("boutique.html", produits=produits)


@app.route("/personnalisation")
def personnalisation():
    return render_template("personnalisation.html")


@app.route("/panier")
def panier():
    if "utilisateur_id" not in session:
        return redirect("/connexion")
    return render_template("panier.html")


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

        return redirect("/connexion")

    return render_template("inscription.html")


@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
