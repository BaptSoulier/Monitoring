import os
import stat
import logging
from core.utils import symbolic_to_octal

def get_permissions(filepath):
    """
    Récupère les permissions d'un fichier.

    Args:
        filepath (str): Le chemin du fichier.

    Returns:
        str: Les permissions du fichier au format symbolique (e.g., "rwxr-xr--"),
             ou None en cas d'erreur.
    """
    try:
        mode = os.stat(filepath).st_mode
        return octal_to_symbolic(stat.S_IMODE(mode))
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des permissions de {filepath}: {e}")
        return None

def set_permissions(filepath, mode):
    """
    Modifie les permissions d'un fichier.

    Args:
        filepath (str): Le chemin du fichier.
        mode (int): Le mode de permission au format octal (e.g., 0o755).

    Returns:
        bool: True si les permissions ont été modifiées avec succès, False sinon.
    """
    try:
        os.chmod(filepath, mode)
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la modification des permissions de {filepath} vers {mode}: {e}")
        return False

def octal_to_symbolic(mode):
    """Convertit un mode octal (nombre) en représentation symbolique (chaîne).

    Args:
        mode (int): Le mode de fichier au format octal (e.g., 0o755).

    Returns:
        str: La représentation symbolique du mode (e.g., 'rwxr-xr-x').
    """
    # Convertit le mode octal en une chaîne de 4 chiffres (e.g., '0755')
    mode_str = f"{mode:04o}"
    # Ignore le premier chiffre (type de fichier) pour les permissions
    mode_str = mode_str[1:]

    # Initialise la chaîne symbolique avec des tirets
    symbolic = "---------";

    # Définit les permissions pour chaque catégorie (propriétaire, groupe, autres)
    for i in range(3):
        octal_digit = int(mode_str[i])
        if octal_digit & 4:  # Lecture
            symbolic = symbolic[:i * 3] + 'r' + symbolic[i * 3 + 1:]
        if octal_digit & 2:  # Écriture
            symbolic = symbolic[:i * 3 + 1] + 'w' + symbolic[i * 3 + 2:]
        if octal_digit & 1:  # Exécution
            symbolic = symbolic[:i * 3 + 2] + 'x' + symbolic[i * 3 + 3:]
    return symbolic