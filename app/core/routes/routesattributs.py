import json
from flask import (
    # Blueprint,
    request,
    current_app,
    session,
    send_from_directory,
    redirect,
    make_response,
    Response,
    render_template,
)
from utils_flask_sqla.response import to_csv_resp, to_json_resp, csv_resp, json_resp
from flask.views import MethodView

# import marshmallow as ma
from flask_smorest import Blueprint, abort

from pypnusershub import routes as fnauth

from app.core.repositories.repository import GenericRepository, BibThemeRepository
from app.core.schemas.schemas_models import (
    TaxrefSchema,
    TaxrefDetailSchema,
    BibThemeSchema,
    BibAttributsSchema,
)
from app.core.schemas.schemas_requests import (
    BibAttributesQueryArgsSchema,
    GenericQueryArgsSchema,
)
from app.core.models.models import BibAttributs, BibTheme

from app.utils.env import DB, LOG, MA

blp = Blueprint(
    "Attributs",
    "Attributs de taxref",
    url_prefix="/pets",
    description="Operations on attibutes",
)


@blp.route("/")
class BibThemeView(MethodView):
    @blp.response(BibThemeSchema(many=True))
    # @blp.arguments(GenericQueryArgsSchema, location='query')
    @blp.arguments(BibAttributesQueryArgsSchema, location="query")
    @blp.paginate()
    def get(self, regne, pagination_parameters):
        """List des attributs avec filtre par règne et group2_inpn"""
        return BibThemeRepository().get_with_regne_grp2_inpn(**regne)


@blp.route("/<id_attribut>")
class AttributView(MethodView):
    @blp.arguments(GenericQueryArgsSchema, location="query")
    @blp.response(BibAttributsSchema(many=False))
    def get(self, id_attribut, args):
        """Détail d'un attribut"""
        return BibAttributs.get(id_attribut)
