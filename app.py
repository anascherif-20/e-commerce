from flask import Flask, render_template, request, redirect
from database import cursor, db

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/boutique")
def boutique():
    categorie = request.args.get("categorie")

    if categorie:
        cursor.execute(
            "SELECT * FROM produits WHERE categorie = %s",
            (categorie,)
        )
    else:
        cursor.execute("SELECT * FROM produits")

    produits = cursor.fetchall()
    return render_template("boutique.html", produits=produits)


@app.route("/personnalisation")
def personnalisation():
    return render_template("personnalisation.html")


@app.route("/panier")
def panier():
    return render_template("panier.html")


@app.route("/connexion")
def connexion():
    return render_template("connexion.html")


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]

        cursor.execute(
            """
            INSERT INTO utilisateurs
            (nom, prenom, email, mot_de_passe)
            VALUES (%s, %s, %s, %s)
            """,
            (nom, prenom, email, mot_de_passe)
        )

        db.commit()
        return redirect("/connexion")

    return render_template("inscription.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)