from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, g
import os
from core.file_watcher import start_monitoring, load_watched_files, save_watched_files
from core.permission_manager import get_permissions, set_permissions, octal_to_symbolic, symbolic_to_octal
from webapp.forms import AddFileForm, ChangePermissionsForm, DeleteFileForm
from core.utils import is_valid_path, calculate_checksum
import logging
import subprocess 
from bson import ObjectId
from datetime import datetime

main_bp = Blueprint('main', __name__)

def get_mongo():
    """Obtient la connexion MongoDB à partir de l'objet global g."""
    if 'mongo' not in g:
        g.mongo = current_app.extensions['pymongo'].db
    return g.mongo

@main_bp.route('/')
def index():
    watched_files = load_watched_files()
    # Récupérer les logs depuis MongoDB, les plus récents en premier
    mongo = get_mongo()
    logs = list(mongo.logs.find().sort('timestamp', -1).limit(100))
    # Convertir les ObjectId en string pour le template
    for log in logs:
        log['_id'] = str(log['_id'])
        log['timestamp'] = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', files=watched_files, logs=logs)

@main_bp.route('/add_file', methods=['GET', 'POST'])
def add_file():
    form = AddFileForm()
    if form.validate_on_submit():
        file_path = form.file_path.data
        if is_valid_path(file_path):
            watched_files = load_watched_files()
            if file_path not in watched_files:
                watched_files.append(file_path)
                save_watched_files(watched_files)
                flash(f"Fichier ajouté pour surveillance : {file_path}", 'success')
            else:
                flash(f"Le fichier {file_path} est déjà surveillé.", 'warning')
            return redirect(url_for('main.index'))
        else:
            flash("Chemin de fichier invalide.", 'danger')
    return render_template('add_file.html', form=form)

@main_bp.route('/delete_file', methods=['POST'])
def delete_file():
    form = DeleteFileForm()
    if form.validate_on_submit():
        file_path = form.file_path.data
        watched_files = load_watched_files()
        if file_path in watched_files:
            watched_files.remove(file_path)
            save_watched_files(watched_files)
            flash(f"Fichier supprimé de la surveillance : {file_path}", 'success')
        else:
            flash(f"Le fichier {file_path} n'est pas surveillé.", 'warning')
        return redirect(url_for('main.index'))
    else:
        flash("Erreur lors de la suppression du fichier.", 'danger')
        return redirect(url_for('main.index'))

@main_bp.route('/permissions/<path:filepath>', methods=['GET', 'POST'])
def permissions(filepath):
    form = ChangePermissionsForm()
    try:
        perms = get_permissions(filepath)
        if perms is None:
            flash("Impossible de récupérer les permissions du fichier.", 'danger')
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            if form.octal_mode.data:
                try:
                    octal_mode = int(form.octal_mode.data, 8)
                    if set_permissions(filepath, octal_mode):
                        flash("Permissions mises à jour avec succès.", 'success')
                        return redirect(url_for('main.index'))
                    else:
                        flash("Erreur lors de la mise à jour des permissions.", 'danger')
                except ValueError:
                    flash("Mode octal invalide.", 'danger')
            else:
                # Traiter les permissions symboliques
                symbolic_mode = ""
                symbolic_mode += "r" if form.owner_read.data else "-"
                symbolic_mode += "w" if form.owner_write.data else "-"
                symbolic_mode += "x" if form.owner_execute.data else "-"
                symbolic_mode += "r" if form.group_read.data else "-"
                symbolic_mode += "w" if form.group_write.data else "-"
                symbolic_mode += "x" if form.group_execute.data else "-"
                symbolic_mode += "r" if form.others_read.data else "-"
                symbolic_mode += "w" if form.others_write.data else "-"
                symbolic_mode += "x" if form.others_execute.data else "-"

                octal_mode = symbolic_to_octal(symbolic_mode)
                if set_permissions(filepath, octal_mode):
                    flash("Permissions mises à jour avec succès.", 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash("Erreur lors de la mise à jour des permissions.", 'danger')

        checksum = calculate_checksum(filepath)
        return render_template('permissions.html', filepath=filepath, permissions=perms, form=form, checksum=checksum)
    except Exception as e:
        flash(f"Erreur : {e}", 'danger')
        return redirect(url_for('main.index'))

@main_bp.route('/checksum/<path:filepath>')
def checksum(filepath):
    """
    Calcule le checksum actuel du fichier et le compare avec le checksum stocké dans MongoDB.
    """
    try:
        current_checksum = calculate_checksum(filepath)
        mongo = get_mongo()
        #  Récupérer le checksum stocké depuis MongoDB
        file_data = mongo.files.find_one({'filepath': filepath}) 
        stored_checksum = file_data.get('checksum') if file_data else None

        if stored_checksum and current_checksum == stored_checksum:
            return jsonify({'status': 'unchanged', 'checksum': current_checksum})
        else:
            # Mettre à jour le checksum dans MongoDB
            mongo.files.update_one(
                {'filepath': filepath},
                {'$set': {'checksum': current_checksum, 'last_modified': datetime.now()}},
                upsert=True  # Insérer un nouveau document si le fichier n'existe pas
            )
            return jsonify({'status': 'changed', 'checksum': current_checksum, 'stored_checksum': stored_checksum})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})

# Flask CLI
@main_bp.cli.command('monitor')
def monitor_command():
    """
    Interface en ligne de commande pour ajouter et supprimer des fichiers à surveiller.
    """
    while True:
        print("\nMoniteur de fichiers en ligne de commande:")
        print("1. Ajouter un fichier à surveiller")
        print("2. Supprimer un fichier de la surveillance")
        print("3. Quitter")
        choix = input("Entrez votre choix : ")

        if choix == '1':
            file_path = input("Entrez le chemin du fichier à surveiller : ")
            if is_valid_path(file_path):
                watched_files = load_watched_files()
                if file_path not in watched_files:
                    watched_files.append(file_path)
                    save_watched_files(watched_files)
                    print(f"Fichier ajouté pour surveillance : {file_path}")
                else:
                    print(f"Le fichier {file_path} est déjà surveillé.")
            else:
                print("Chemin de fichier invalide.")
        elif choix == '2':
            file_path = input("Entrez le chemin du fichier à supprimer de la surveillance : ")
            watched_files = load_watched_files()
            if file_path in watched_files:
                watched_files.remove(file_path)
                save_watched_files(watched_files)
                print(f"Fichier supprimé de la surveillance : {file_path}")
            else:
                print(f"Le fichier {file_path} n'est pas surveillé.")
        elif choix == '3':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
