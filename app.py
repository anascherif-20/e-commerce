from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/boutique")
def boutique():
    return render_template("boutique.html")

@app.route("/personnalisation")
def personnalisation():
    return render_template("personnalisation.html")

@app.route("/panier")
def panier():
    return render_template("panier.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)