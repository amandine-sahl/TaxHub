from server import db,init_app
from werkzeug.utils import secure_filename

import os
import unicodedata
import re

def remove_file(filepath):
    try :
        os.remove(os.path.join(init_app().config['BASE_DIR'], filepath))
    except :
        pass

def rename_file(old_chemin, old_title, new_title):
    try :
        new_chemin = old_chemin.replace(removeDisallowedFilenameChars(old_title),removeDisallowedFilenameChars(new_title))
        os.rename(old_chemin, new_chemin)
        return new_chemin
    except :
        pass

def upload_file(file, id_media, cd_ref, titre):
    filename = str(cd_ref)+ '_' + str(id_media) + '_' + removeDisallowedFilenameChars(titre) + '.' + file.filename.rsplit('.', 1)[1]
    filepath = os.path.join(init_app().config['UPLOAD_FOLDER'], filename)
    file.save(os.path.join(init_app().config['BASE_DIR'], filepath))
    return filepath


def removeDisallowedFilenameChars(uncleanString):
    cleanedString = secure_filename(uncleanString)
    cleanedString = unicodedata.normalize('NFKD', uncleanString).encode('ASCII', 'ignore')
    cleanedString = cleanedString.decode("utf-8")
    cleanedString = re.sub('[ ]+', '_', cleanedString)
    cleanedString = re.sub('[^0-9a-zA-Z_-]', '', cleanedString)
    return cleanedString
