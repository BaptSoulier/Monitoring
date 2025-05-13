from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Regexp

class AddFileForm(FlaskForm):
    file_path = StringField('Chemin du fichier', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class ChangePermissionsForm(FlaskForm):
    owner_read = BooleanField('Lecture (Propriétaire)')
    owner_write = BooleanField('Écriture (Propriétaire)')
    owner_execute = BooleanField('Exécution (Propriétaire)')
    group_read = BooleanField('Lecture (Groupe)')
    group_write = BooleanField('Écriture (Groupe)')
    group_execute = BooleanField('Exécution (Groupe)')
    others_read = BooleanField('Lecture (Autres)')
    others_write = BooleanField('Écriture (Autres)')
    others_execute = BooleanField('Exécution (Autres)')
    
    # Octal mode (alternative)
    octal_mode = StringField('Mode Octal (e.g., 755)', validators=[Optional(), Regexp(r'^[0-7]{3,4}$', message='Invalid octal mode')])

    submit = SubmitField('Changer les Permissions')
    
class DeleteFileForm(FlaskForm): 
    file_path = StringField('Chemin du fichier', validators=[DataRequired()])
    submit = SubmitField('Supprimer')
