import marshmallow as ma
from app.core.models.models import VmTaxrefHierarchie


class GenericQueryArgsSchema(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.INCLUDE


class BibAttributesQueryArgsSchema(GenericQueryArgsSchema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    regne = ma.fields.String(missing=None)
    group2_inpn = ma.fields.String(missing=None)


class TaxrefSearchTrg(GenericQueryArgsSchema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    add_rank = ma.fields.String(missing=None)
    rank_limit = ma.fields.String(missing=None)
