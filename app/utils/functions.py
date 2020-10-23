'''
    Fichier contenant des fonctions utilisées
    par l'ensemble de l'application
'''

import marshmallow as ma
# from marshmallow import Schema, fields


# With marshmallow 3, define unknown=EXCLUDE
class GenericQueryArgsSchema(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE
    regne = ma.fields.String(missing=None)
    group2_inpn = ma.fields.String(missing=None)



def calculate_offset_page(limit, offset, page):
    """
        fonction qui calcul les paramètres
            offset et page
        Si un offset est défini
            il prend le pas sur le paramètre page
        Le paramètre page est seulement indicatif, il commence à 1 et ne peut être < 1
        Le offset commence à 0 et ne peut pas être négatif
    """
    if offset:
        if offset < 0:
            offset = 0
        page = int(offset / limit)
        return (limit, offset, page)
    else:
        page = 1 if page < 1  else page
        offset = (page-1) * limit
        return (limit, offset, page)