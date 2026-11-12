import os


class Config:
    """Configuration de l'application TransFormateur."""

    FORMATS_SUPPORTES = ["csv", "json", "xml", "md"]

    CONVERSIONS_DISPONIBLES = [
        ("csv", "json"),
        ("json", "csv"),
        ("csv", "xml"),
        ("xml", "csv"),
        ("json", "xml"),
        ("xml", "json"),
        ("md", "html"),
    ]

    TAILLE_MAX_OCTETS = 2 * 1024 * 1024  # 2 Mo

    def __init__(self):
        self.dossier_upload = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(self.dossier_upload, exist_ok=True)
