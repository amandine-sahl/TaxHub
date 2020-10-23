from app.utils.env import MA
from marshmallow import EXCLUDE, pre_load, post_load, pre_dump, fields, ValidationError
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter

from app.core.models.models import (
    Taxref,
    BibListe,
    CorTaxonAttribut,
    TMedia,
    BibAttributs,
    BibTheme,
)


class TMediaSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = TMedia


class BibAttributsSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = BibAttributs

    # theme = MA.Nested(
    #     lambda : BibThemeSchema(exclude=("attributs",))
    # )


class BibListeSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = BibListe


class CorTaxonAttributSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = CorTaxonAttribut
        include_fk = True


class BibThemeSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = BibTheme
        include_fk = True

    attributs = MA.Nested(BibAttributsSchema, many=True)


class TaxrefSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = Taxref
        include_fk = True
        load_instance = True
        unknown = EXCLUDE

    nb_listes = fields.Function(lambda obj: len(obj.bib_listes))
    nb_attr = fields.Function(lambda obj: len(obj.attributs))
    nb_media = fields.Function(lambda obj: len(obj.medias))


class TaxrefDetailSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = Taxref
        include_fk = True
        load_instance = True
        unknown = EXCLUDE

    bib_listes = MA.Nested(
        BibListeSchema,
        many=True,
        # only=("id_liste", "code_liste", "nom_liste")
    )
    attributs = MA.Nested(
        CorTaxonAttributSchema, many=True, only=("id_attribut", "valeur_attribut")
    )
    medias = MA.Nested(TMediaSchema, many=True)
