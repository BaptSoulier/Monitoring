import os
import hashlib
import stat

def is_valid_path(file_path):
    """
    Vérifie si le chemin du fichier est valide.

    Args:
        file_path (str): Le chemin du fichier à vérifier.

    Returns:
        bool: True si le chemin est valide, False sinon.
    """
    if not file_path:
        return False
    # Ajout de la vérification de l'existence du répertoire
    directory = os.path.dirname(file_path)
    if directory and not os.path.isdir(directory):
        return False
    return os.path.exists(file_path)

def calculate_checksum(file_path):
    """
    Calcule le checksum SHA-256 d'un fichier.

    Args:
        file_path (str): Le chemin du fichier.

    Returns:
        str: Le checksum SHA-256 du fichier, ou None en cas d'erreur.
    """
    if not os.path.exists(file_path):
        return None
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(4096) 
                if not chunk:
                    break
                hasher.update(chunk)
    except Exception as e:
        print(f"Erreur lors du calcul du checksum : {e}")
        return None
    return hasher.hexdigest()

def symbolic_to_octal(symbolic_mode):
    """
    Convertit un mode de permission symbolique (rwxrwxrwx) en mode octal (e.g., 755).

    Args:
        symbolic_mode (str): Le mode de permission symbolique (e.g., "rwxr-xr--").

    Returns:
        int: Le mode de permission octal (e.g., 754).
    """
    if len(symbolic_mode) != 9:
        raise ValueError("Invalid symbolic mode. Must be 9 characters long.")

    def _get_octal_value(permissions):
        value = 0
        if permissions[0] == 'r':
            value += 4
        if permissions[1] == 'w':
            value += 2
        if permissions[2] == 'x':
            value += 1
        return value

    owner_octal = _get_octal_value(symbolic_mode[0:3])
    group_octal = _get_octal_value(symbolic_mode[3:6])
    others_octal = _get_octal_value(symbolic_mode[6:9])

    return int(f"{owner_octal}{group_octal}{others_octal}", 8)