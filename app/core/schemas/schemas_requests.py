import marshmallow as ma
from app.core.models.models import VmTaxrefHierarchie


class GenericQueryArgsSchema(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.INCLUDE


class BibAttributesQueryArgsSchema(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    regne = ma.fields.String(missing=None)
    group2_inpn = ma.fields.String(missing=None)


class BibAttributesQueryArgsSchema(ma.Schema):
    class Meta:
        ordered = True
        unknown = ma.EXCLUDE

    regne = ma.fields.String(missing=None)
    group2_inpn = ma.fields.String(missing=None)
