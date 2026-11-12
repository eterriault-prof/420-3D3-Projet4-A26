import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from config import Config
from convertisseurs import get_convertisseur

app = Flask(__name__)
app.secret_key = "transformateur-secret"

config = Config()


@app.route("/")
def index():
    return render_template(
        "index.html",
        conversions=Config.CONVERSIONS_DISPONIBLES,
    )


@app.route("/convertir", methods=["POST"])
def convertir():
    fichier = request.files.get("fichier")
    format_cible = request.form.get("format_cible")

    if not fichier or fichier.filename == "":
        flash("Veuillez sélectionner un fichier.")
        return redirect(url_for("index"))

    extension = fichier.filename.rsplit(".", 1)[-1].lower()

    if (extension, format_cible) not in Config.CONVERSIONS_DISPONIBLES:
        flash(f"Conversion {extension} → {format_cible} non supportée.")
        return redirect(url_for("index"))

    contenu = fichier.read()
    if len(contenu) > Config.TAILLE_MAX_OCTETS:
        flash("Fichier trop volumineux (max 2 Mo).")
        return redirect(url_for("index"))

    try:
        convertisseur = get_convertisseur(extension, format_cible)
        resultat = convertisseur.convertir(contenu.decode("utf-8"))
    except Exception as e:
        flash(f"Erreur lors de la conversion : {e}")
        return redirect(url_for("index"))

    nom_base = fichier.filename.rsplit(".", 1)[0]
    nom_sortie = f"{nom_base}.{format_cible}"
    chemin_sortie = os.path.join(config.dossier_upload, nom_sortie)

    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write(resultat)

    return send_file(chemin_sortie, as_attachment=True, download_name=nom_sortie)


if __name__ == "__main__":
    app.run(debug=True)
