
from flask import Flask, render_template

app = Flask(__name__)

produits = [
    {
        "id": 1,
        "nom": "Bracelet Rose Perlé",
        "prix": 12.99,
        "image": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?w=600",
        "description": "Bracelet fait main avec des perles roses."
    },
    {
        "id": 2,
        "nom": "Bracelet Bleu Ciel",
        "prix": 10.99,
        "image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600",
        "description": "Bracelet doux et élégant aux couleurs bleues."
    },
    {
        "id": 3,
        "nom": "Bracelet Doré",
        "prix": 14.99,
        "image": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600",
        "description": "Bracelet artisanal avec finition dorée."
    }
]

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/boutique")
def boutique():
    return render_template("boutique.html", produits=produits)

if __name__ == "__main__":
    app.run(debug=True, port=5001)