import copy

from sqlalchemy import select, or_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from app.core.models.models import Taxref, CorTaxonAttribut, BibTheme, BibAttributs
from app.core.schemas.schemas_models import TaxrefSchema
from app.core.schemas.schema_utils import NUMBER_OPERATORS, DATE_OPERATORS
from app.utils.functions import calculate_offset_page
from app.utils.env import DB, LOG, MA

# https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperator
MAPPING_OPERATOR_TEXT_TO_SQLA = {
    "ne": "ne",
    "gt": "gt",
    "ge": "ge",
    "lt": "lt",
    "le": "le",
}


class GenericRepository:
    """
    Repository: classe permettant l'acces au données
    d'un modèle de type 'releve'
    """

    def __init__(
        self,
        model,
    ):
        self._model = model
        self._model_col = model.__table__.columns

    def get_all(self, pagination, params=None):
        """
        Retourne un ensemble de résultat
        """
        (limit, offset, page) = self.process_pagination(pagination)
        try:
            q = DB.session.query(self._model)
            if params:
                q, used_params = self.build_generic_filter(q, params)
            count = q.count()
            return (count, q.limit(limit).offset(offset).all())
        except Exception as e:
            LOG.error(str(e))
            raise (e)

    def get_one(self, id):
        try:
            return DB.session.query(self._model).get(id)
        except MultipleResultsFound:
            LOG.error(f"Mutliple row found")
        else:
            return True

    def get_distinct_field(self, field_name, limit=100, offset=0):
        # Test field exist in model
        if not self.field_exists(field_name):
            LOG.error(f"Field {field_name} don't exists")
            raise Exception(f"Field {field_name} don't exists")
        try:
            return (
                DB.session.query(self._model.__table__.columns[field_name])
                .distinct()
                .limit(limit)
                .offset(offset)
                .all()
            )
        except Exception as e:
            LOG.error(str(e))
            raise (e)

    def field_exists(self, field_name):
        if field_name in self._model_col:
            return True
        return False

    def build_generic_filter(self, query, params):
        copy_params = dict(copy.deepcopy(params))

        for param in params:
            query, used = self.build_query_filter(query, param, params[param])
            if used:
                copy_params.pop(param)
        print(query)
        query, params = self.build_order_query(query, params)
        return query, params

    def build_query_filter(self, query, param_name, param_value):

        # Split extra opérateur
        col_name = param_name.split("__")
        filter_op = None

        # S'il y a un opérateur de filtre
        if len(col_name) > 1:
            (col_name, filter_op) = col_name

        # Si le paramètre n'est pas reconnu comme una attribut du model
        if not col_name in self._model_col.keys():
            return query, False

        # Récupération de la propriété du modèle
        col = self._model_col[col_name]

        if not filter_op:
            # S'il n'y a pas d'opérateur de filtre : recherche exacte
            query = query.filter(self._model_col[param_name] == param_value)

        elif filter_op == "ilike":
            # Si l'opérateur de filtre est ilike
            query = query.filter(col.ilike("%{}%".format(param_value)))

        elif MAPPING_OPERATOR_TEXT_TO_SQLA[filter_op]:
            # Si l'opérateur de filtre est un opérateur de comparaison générique
            # TODO Missing test data type ?? est-ce utile dans le contexte des schémas marsmallow
            try:
                sql_op = MAPPING_OPERATOR_TEXT_TO_SQLA[filter_op]
                # Récupération de l'opérateur de (ColumnOperators) de la colonne
                attr = (
                    list(
                        filter(
                            lambda e: hasattr(col, e % sql_op), [
                                "%s", "%s_", "__%s__"]
                        )
                    )[0]
                    % sql_op
                )
            except IndexError:
                raise Exception("Invalid filter operator: %s" % filter_op)
            # Construction du filtre
            filt = getattr(col, attr)(param_value)
            query = query.filter(filt)

        return query, True

    def filter_or_none(self, query, field, value):
        return query.filter(
            or_(self._model_col[field] == value,
                self._model_col[field] == None)
        )

    def build_order_query(self, query, params):
        # Order by
        if "orderby" in params:
            if params["orderby"] in self._model_col:
                orderCol = getattr(self._model_col, params["orderby"])
                params.pop("orderby")
            else:
                orderCol = None
            if "order" in params:
                if params["order"] == "desc":
                    orderCol = orderCol.desc()
                params.pop("order")
            query = query.order_by(orderCol)

        return query, params

    def process_pagination(self, pagination_params):
        return calculate_offset_page(
            pagination_params.page_size, None, pagination_params.page
        )


class TaxrefRepository(GenericRepository):
    def __init__(self):
        super().__init__(Taxref)

    def build_generic_filter(self, query, params):
        query, copy_params = super().build_generic_filter(query, params)

        if copy_params.get("is_ref", "false") == "true":
            query = query.filter(self._model.cd_nom == self._model.cd_ref)
            copy_params.pop("is_ref")

        if copy_params.get("has_attributes", "false") == "true":
            query = query.join(self._model.attributs)
            copy_params.pop("has_attributes")

        return query, copy_params


class BibThemeRepository(GenericRepository):
    def __init__(self):
        super().__init__(BibTheme)

    def get_with_regne_grp2_inpn(self, regne, group2_inpn):
        try:
            query = DB.session.query(self._model).join(self._model.attributs)
            attributs_rep = GenericRepository(BibAttributs)
            if regne:
                query = attributs_rep.filter_or_none(query, "regne", regne)
            if group2_inpn:
                query = attributs_rep.filter_or_none(
                    query, "group2_inpn", group2_inpn)

            return query.all()

        except Exception as e:
            LOG.error(str(e))
            raise (e)
