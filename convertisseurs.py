import csv
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import io


# ---------------------------------------------------------------------------
# Classes de conversion — sans hiérarchie commune
# ---------------------------------------------------------------------------

class CsvVersJson:
    def convertir(self, contenu: str) -> str:
        lecteur = csv.DictReader(io.StringIO(contenu))
        lignes = list(lecteur)
        return json.dumps(lignes, ensure_ascii=False, indent=2)


class JsonVersCsv:
    def convertir(self, contenu: str) -> str:
        donnees = json.loads(contenu)
        if not donnees:
            return ""
        sortie = io.StringIO()
        ecrivain = csv.DictWriter(sortie, fieldnames=donnees[0].keys())
        ecrivain.writeheader()
        ecrivain.writerows(donnees)
        return sortie.getvalue()


class CsvVersXml:
    def convertir(self, contenu: str) -> str:
        lecteur = csv.DictReader(io.StringIO(contenu))
        racine = ET.Element("donnees")
        for ligne in lecteur:
            enregistrement = ET.SubElement(racine, "enregistrement")
            for cle, valeur in ligne.items():
                enfant = ET.SubElement(enregistrement, cle)
                enfant.text = valeur
        brut = ET.tostring(racine, encoding="unicode")
        return xml.dom.minidom.parseString(brut).toprettyxml(indent="  ")


class XmlVersCsv:
    def convertir(self, contenu: str) -> str:
        racine = ET.fromstring(contenu)
        enregistrements = list(racine)
        if not enregistrements:
            return ""
        colonnes = [e.tag for e in enregistrements[0]]
        sortie = io.StringIO()
        ecrivain = csv.DictWriter(sortie, fieldnames=colonnes)
        ecrivain.writeheader()
        for enr in enregistrements:
            ecrivain.writerow({e.tag: e.text for e in enr})
        return sortie.getvalue()


class JsonVersXml:
    def convertir(self, contenu: str) -> str:
        donnees = json.loads(contenu)
        racine = ET.Element("donnees")
        for item in donnees:
            enregistrement = ET.SubElement(racine, "enregistrement")
            for cle, valeur in item.items():
                enfant = ET.SubElement(enregistrement, cle)
                enfant.text = str(valeur)
        brut = ET.tostring(racine, encoding="unicode")
        return xml.dom.minidom.parseString(brut).toprettyxml(indent="  ")


class XmlVersJson:
    def convertir(self, contenu: str) -> str:
        racine = ET.fromstring(contenu)
        donnees = []
        for enr in racine:
            donnees.append({e.tag: e.text for e in enr})
        return json.dumps(donnees, ensure_ascii=False, indent=2)


class MarkdownVersHtml:
    def convertir(self, contenu: str) -> str:
        lignes = contenu.splitlines()
        html = []
        in_list = False
        for ligne in lignes:
            if ligne.startswith("# "):
                if in_list:
                    html.append("</ul>")
                    in_list = False
                html.append(f"<h1>{ligne[2:]}</h1>")
            elif ligne.startswith("## "):
                if in_list:
                    html.append("</ul>")
                    in_list = False
                html.append(f"<h2>{ligne[3:]}</h2>")
            elif ligne.startswith("### "):
                if in_list:
                    html.append("</ul>")
                    in_list = False
                html.append(f"<h3>{ligne[4:]}</h3>")
            elif ligne.startswith("- ") or ligne.startswith("* "):
                if not in_list:
                    html.append("<ul>")
                    in_list = True
                html.append(f"  <li>{ligne[2:]}</li>")
            elif ligne.strip() == "":
                if in_list:
                    html.append("</ul>")
                    in_list = False
                html.append("")
            else:
                if in_list:
                    html.append("</ul>")
                    in_list = False
                html.append(f"<p>{ligne}</p>")
        if in_list:
            html.append("</ul>")
        return "\n".join(html)


# ---------------------------------------------------------------------------
# Fonction de sélection du convertisseur — if/elif en cascade
# ---------------------------------------------------------------------------

def get_convertisseur(format_source: str, format_cible: str):
    if format_source == "csv" and format_cible == "json":
        return CsvVersJson()
    elif format_source == "json" and format_cible == "csv":
        return JsonVersCsv()
    elif format_source == "csv" and format_cible == "xml":
        return CsvVersXml()
    elif format_source == "xml" and format_cible == "csv":
        return XmlVersCsv()
    elif format_source == "json" and format_cible == "xml":
        return JsonVersXml()
    elif format_source == "xml" and format_cible == "json":
        return XmlVersJson()
    elif format_source == "md" and format_cible == "html":
        return MarkdownVersHtml()
    else:
        raise ValueError(f"Conversion non supportée : {format_source} → {format_cible}")
