from flask_smorest import Page
import json
from flask import (
    Blueprint,
    request,
    current_app,
    session,
    send_from_directory,
    redirect,
    make_response,
    Response,
    render_template,
    jsonify,
)
from flask.views import MethodView
from app.core.repositories.repository import TaxrefRepository, GenericRepository
from app.core.schemas.schemas_models import TaxrefSchema, TaxrefDetailSchema, TaxrefSeachTrgSchema
from app.core.schemas.schemas_requests import GenericQueryArgsSchema,TaxrefSearchTrg
from app.core.schemas.schema_utils import generic_model_schema, generic_query_schema
from app.core.models.models import VmTaxrefHierarchie

from app.utils.env import DB, LOG, MA

from flask_smorest import Blueprint, abort

blp = Blueprint(
    "Taxref", "Taxref", url_prefix="/taxref", description="Operations on taxref table"
)


@blp.route("/")
class TaxrefView(MethodView):
    @blp.response(TaxrefSchema(many=True))
    @blp.arguments(TaxrefSchema, location="query")
    @blp.arguments(GenericQueryArgsSchema, location="query")
    @blp.paginate()
    def get(self, taxrefargs, extraargs, pagination_parameters):
        """Liste des données de taxref """
        count, data = TaxrefRepository().get_all(
            pagination_parameters, TaxrefSchema().dump(taxrefargs)
        )
        pagination_parameters.item_count = count
        return jsonify(TaxrefSchema().dump(data, many=True))


VmTaxrefHierarchieSchema = generic_model_schema(VmTaxrefHierarchie)


@blp.route("/hierachie")
class TaxrefHierarchieView(MethodView):
    @blp.response(VmTaxrefHierarchieSchema(many=True))
    @blp.arguments(
        generic_query_schema(
            VmTaxrefHierarchie,
            _fields_filters={"lb_nom": ("string",)},
        ),
        location="query",
    )
    @blp.paginate()
    def get(self, args, pagination_parameters):
        """Liste des données de la hiérarchie taxonomique de taxref """
        count, data = GenericRepository(VmTaxrefHierarchie).get_all(
            pagination_parameters, args
        )
        pagination_parameters.item_count = count
        if args["only_field"]:
            return jsonify(
                VmTaxrefHierarchieSchema(
                    only=args["only_field"]).dump(data, many=True)
            )
        return data


@blp.route("/search/<field>/<ilike>")
class TaxrefSearchView(MethodView):
    @blp.response(TaxrefSeachTrgSchema(many=True))
    @blp.arguments(TaxrefSearchTrg, location='query', as_kwargs=True)
    def get(self, field, ilike,  **kwargs):
        """
        Get the first 20 result of Taxref table for a given field with an ilike query
        Use trigram algo to add relevance
            :params field: a Taxref column
            :type field: str
            :param ilike: the ilike where expression to filter
            :type ilike:str
            :query str add_rank: join on table BibTaxrefRank and add the column 'nom_rang' to the result
            :query str rank_limit: return only the taxon where rank <= of the given rank (id_rang of BibTaxrefRang table)
            :returns: Array of dict
        """
        # TODO add test and optimize
        count, data = TaxrefRepository().search_trg(field, ilike, kwargs)
        return TaxrefSeachTrgSchema(many=True).dump(data)
        