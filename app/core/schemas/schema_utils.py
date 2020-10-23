from copy import deepcopy


from marshmallow import (
    EXCLUDE,
    pre_load,
    post_load,
    pre_dump,
    fields,
    ValidationError,
    SchemaOpts,
    schema,
)
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import (
    SQLAlchemyAutoSchemaOpts,
    SQLAlchemyAutoSchemaMeta,
)

from app.utils.env import MA


NUMBER_OPERATORS = DATE_OPERATORS = ("ne", "gt", "ge", "lt", "le")

STRING_OPERATORS = (
    "ilike",
    # 'contains', 'icontains', 'startswith', 'istartswith',
    # 'endswith', 'iendswith', 'iexact'
)

QUERY_OPERATORS = {
    "number": NUMBER_OPERATORS,
    "string": STRING_OPERATORS,
    "date": DATE_OPERATORS,
}


def generic_model_schema(_model):
    """
    Fonction permettant de généré à la volé
        un schéma à partir d'un model sqlalchemy

    :params: _model(DB.Model) : Classe du model

    :return: return schema autogenéré
    :rtype: (MA.SQLAlchemyAutoSchema

    """

    class Schema(MA.SQLAlchemyAutoSchema):
        class Meta:
            model = _model
            unknown = EXCLUDE

    return Schema


class FiltersSchemaOpts(SQLAlchemyAutoSchemaOpts):
    """
    Surcharge de la classe SQLAlchemyAutoSchemaOpts
    permettant de rajouter un attribut fields_filters
    """

    def __init__(self, meta, ordered=False):
        super().__init__(meta, ordered)
        # Add a new meta field to pass the list of filters
        self.fields_filters = getattr(meta, "fields_filters", None)


class FiltersSchemaMeta(SQLAlchemyAutoSchemaMeta):
    """
    Surcharge de la Metaclass de `SQLAlchemyAutoSchemaMeta`
    """

    @classmethod
    def get_declared_fields(mcs, klass, *args, **kwargs):
        """
        Surcharge de la méthode get_declared_fields de `SQLAlchemyAutoSchemaMeta`

        Permet de rajouter des champs de type "filtre" générique pour les
        champ de type :
            string :
               - ilike
            number
            date

        """

        fields = super().get_declared_fields(klass, *args, **kwargs)

        # Create empty dict using provided dict_class
        declared_fields = kwargs.get("dict_class", dict)()

        # Add base fields
        base_fields = super().get_declared_fields(klass, *args, **kwargs)
        declared_fields.update(base_fields)

        # Get allowed filters from Meta and create filters
        opts = klass.opts
        fields_filters = getattr(opts, "fields_filters", None)

        if fields_filters:
            filter_fields = {}
            for field_name, field_filters in fields_filters.items():
                field = base_fields.get(field_name, None)
                if field:
                    for filter_category in field_filters:
                        for operator in QUERY_OPERATORS.get(filter_category, ()):
                            filter_fields[
                                "{}__{}".format(field_name, operator)
                            ] = deepcopy(field)
            declared_fields.update(filter_fields)

        return declared_fields


def generic_query_schema(_model, _fields_filters):
    """
    Fonction permettant de généré à la volé
        un schéma à partir d'un model sqlalchemy
        et d'y ajouter des filtres génériques

    :params: _model(DB.Model) : Classe du model
    :params: _fields_filters(array) : liste des champs concernés par
         la génération automatique de filtre

    :return: return schema autogenéré
    :rtype: MA.SQLAlchemyAutoSchema

    """

    class Schema(MA.SQLAlchemyAutoSchema, metaclass=FiltersSchemaMeta):
        __metaclass__ = FiltersSchemaMeta

        OPTIONS_CLASS = FiltersSchemaOpts

        class Meta:
            model = _model
            unknown = EXCLUDE
            fields_filters = _fields_filters

        only_field = fields.List(
            fields.String(), missing=[], description="list of fields to return"
        )

        @post_load(pass_many=True)
        def check_only_fields(self, data, many, **kwargs):
            """
            Fonction de validation des paramètres

            - filtre les champs du paramètre only_field
            """
            check_only_field = []
            for field in data["only_field"]:
                if field in self.declared_fields.keys():
                    check_only_field.append(field)

            data["only_field"] = check_only_field
            return data

    return Schema


def generic_query_schema_old(_model):
    class Schema(MA.SQLAlchemyAutoSchema):
        def __init__(self, add_field_filters=None, additional_fields=None, **kwargs):
            super().__init__(**kwargs)
            if not additional_fields:
                additional_fields = {}

            for field in add_field_filters:

                try:
                    original_field = self.declared_fields[field]
                except KeyError:
                    pass
                else:
                    # TODO FINISH
                    # Test type

                    if isinstance(original_field, fields.String):
                        additional_fields[field + "_ilike"] = fields.String(
                            missing=None
                        )

                    # Date
                    # number
            if additional_fields:
                self.declared_fields.update(additional_fields)

        class Meta:
            model = _model
            unknown = EXCLUDE

    return Schema
