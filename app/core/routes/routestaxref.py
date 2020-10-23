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
from app.core.schemas.schemas_models import TaxrefSchema, TaxrefDetailSchema
from app.core.schemas.schemas_requests import GenericQueryArgsSchema
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


# blueprint = Blueprint("pr_occtax", __name__)

# @blueprint.route("/taxref", methods=["GET"])
# @json_resp
# def get_taxref():
#     """
#     Get all Taxref

#     .. :quickref: Taxref;

#     :returns: `dict<Taxref>`
#     """
#     params = dict(request.args)
#     f_data = TaxrefRepository().get_and_fromat('get_all', {"limit": 100, "offset": 0, "params": params}, True)
#     return {
#         "items": f_data
#     }


# @blueprint.route("/taxref/<int:cd_nom>", methods=["GET"])
# @json_resp
# def get_taxref_detail(cd_nom):
#     """
#     Get all Taxref

#     .. :quickref: Taxref;

#     :returns: `dict<Taxref>`
#     """
#     f_data = TaxrefRepository(
#         schema=TaxrefDetailSchema
#     ).get_and_fromat('get_one', {"id": cd_nom}, False)
#     return {
#         "items": f_data
#     }

# @blueprint.route("/distinct/<field>", methods=["GET"])
# @json_resp
# def get_taxref_distinct_field(field):
#     """
#     Get all value for distinct field

#     .. :quickref: Taxref;

#     :returns: `array<Value>`
#     """
#     data = TaxrefRepository().get_distinct_field(field)
#     return [d[0] for d in data]


# @blueprint.route("/allnamebylist/<string:code_liste>", methods=["GET"])
# @json_resp
# def get_all_taxref_name_by_liste(code_liste):
#     pass
