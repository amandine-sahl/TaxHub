from sqlalchemy import (
    BigInteger,
    Boolean,
    CHAR,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.orm import relationship

from app.utils.env import DB


class BibTaxrefStatut(DB.Model):
    __tablename__ = "bib_taxref_statuts"
    __table_args__ = {"schema": "taxonomie"}

    id_statut = DB.Column(DB.Unicode, primary_key=True)
    nom_statut = DB.Column(DB.Unicode, nullable=False)


class BibListe(DB.Model):
    __tablename__ = "bib_listes"
    __table_args__ = {"schema": "taxonomie"}

    id_liste = DB.Column(DB.Integer, primary_key=True)
    code_liste = DB.Column(DB.Unicode, unique=True)
    nom_liste = DB.Column(DB.Unicode, unique=True)
    desc_liste = DB.Column(DB.Unicode)
    picto = DB.Column(DB.Unicode)
    regne = DB.Column(DB.Unicode)
    group2_inpn = DB.Column(DB.Unicode)


class BibTaxrefHabitat(DB.Model):
    __tablename__ = "bib_taxref_habitats"
    __table_args__ = {"schema": "taxonomie"}

    id_habitat = DB.Column(DB.Integer, primary_key=True)
    nom_habitat = DB.Column(DB.Unicode, nullable=False)
    desc_habitat = DB.Column(DB.Unicode)


class BibTaxrefRang(DB.Model):
    __tablename__ = "bib_taxref_rangs"
    __table_args__ = {"schema": "taxonomie"}

    id_rang = DB.Column(DB.Unicode, primary_key=True)
    nom_rang = DB.Column(DB.Unicode, nullable=False)
    tri_rang = DB.Column(DB.Integer)


class BibTheme(DB.Model):
    __tablename__ = "bib_themes"
    __table_args__ = (
        # CheckConstraint('(id_droit >= 0) AND (id_droit <= 6)'),
        {"schema": "taxonomie"}
    )

    id_theme = DB.Column(DB.Integer, primary_key=True)
    nom_theme = DB.Column(DB.Unicode)
    desc_theme = DB.Column(DB.Unicode)
    ordre = DB.Column(DB.Integer)
    id_droit = DB.Column(DB.Integer, server_default=text("0"))

    attributs = relationship("BibAttributs")


class BibTypesMedia(DB.Model):
    __tablename__ = "bib_types_media"
    __table_args__ = {"schema": "taxonomie"}

    id_type = DB.Column(DB.Integer, primary_key=True)
    nom_type_media = DB.Column(DB.Unicode, nullable=False)
    desc_type_media = DB.Column(DB.Unicode)


class BibAttributs(DB.Model):
    __tablename__ = "bib_attributs"
    __table_args__ = {"schema": "taxonomie"}

    id_attribut = DB.Column(DB.Integer, primary_key=True)
    nom_attribut = DB.Column(DB.Unicode, nullable=False)
    label_attribut = DB.Column(DB.Unicode, nullable=False)
    liste_valeur_attribut = DB.Column(DB.Unicode, nullable=False)
    obligatoire = DB.Column(DB.BOOLEAN, nullable=False, server_default=text("false"))
    desc_attribut = DB.Column(DB.Unicode)
    type_attribut = DB.Column(DB.Unicode)
    type_widget = DB.Column(DB.Unicode)
    regne = DB.Column(DB.Unicode)
    group2_inpn = DB.Column(DB.Unicode)
    id_theme = DB.Column(ForeignKey("taxonomie.bib_themes.id_theme"), nullable=False)
    ordre = DB.Column(DB.Integer)

    theme = relationship("BibTheme")


t_cor_nom_liste = Table(
    "cor_nom_liste",
    DB.metadata,
    DB.Column(
        "id_liste",
        ForeignKey("taxonomie.bib_listes.id_liste", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    DB.Column(
        "cd_nom",
        ForeignKey("taxonomie.taxref.cd_nom"),
        primary_key=True,
        nullable=False,
    ),
    schema="taxonomie",
)


class CorTaxonAttribut(DB.Model):
    __tablename__ = "cor_taxon_attribut"
    __table_args__ = (
        CheckConstraint("cd_ref = taxonomie.find_cdref(cd_ref)"),
        {"schema": "taxonomie"},
    )

    id_attribut = DB.Column(
        ForeignKey("taxonomie.bib_attributs.id_attribut"),
        primary_key=True,
        nullable=False,
    )
    cd_ref = DB.Column(
        ForeignKey("taxonomie.taxref.cd_ref"), primary_key=True, nullable=False
    )
    valeur_attribut = DB.Column(DB.Unicode, nullable=False, index=True)

    bib_attribut = relationship("BibAttributs")


class TMedia(DB.Model):
    __tablename__ = "t_medias"
    __table_args__ = {"schema": "taxonomie"}

    id_media = DB.Column(DB.Integer, primary_key=True)
    cd_nom = DB.Column(
        ForeignKey("taxonomie.taxref.cd_nom", onupdate="CASCADE", match="FULL")
    )
    titre = DB.Column(DB.Unicode, nullable=False)
    url = DB.Column(DB.Unicode)
    chemin = DB.Column(DB.Unicode)
    auteur = DB.Column(DB.Unicode)
    desc_media = DB.Column(DB.Unicode)
    date_media = DB.Column(DB.DateTime)
    is_public = DB.Column(DB.BOOLEAN, nullable=False, server_default=text("true"))
    supprime = DB.Column(DB.BOOLEAN, nullable=False, server_default=text("false"))
    id_type = DB.Column(
        ForeignKey(
            "taxonomie.bib_types_media.id_type", onupdate="CASCADE", match="FULL"
        ),
        nullable=False,
    )
    source = DB.Column(DB.Unicode)
    licence = DB.Column(DB.Unicode)

    taxref = relationship("Taxref")
    bib_types_media = relationship("BibTypesMedia")


class Taxref(DB.Model):
    __tablename__ = "taxref"
    __table_args__ = (
        Index("i_taxref_hierarchy", "regne", "phylum", "classe", "ordre", "famille"),
        {"schema": "taxonomie"},
    )

    cd_nom = DB.Column(DB.Integer, primary_key=True)
    id_statut = DB.Column(
        ForeignKey("taxonomie.bib_taxref_statuts.id_statut", onupdate="CASCADE"),
        index=True,
    )
    id_habitat = DB.Column(
        ForeignKey("taxonomie.bib_taxref_habitats.id_habitat", onupdate="CASCADE"),
        index=True,
    )
    id_rang = DB.Column(
        ForeignKey("taxonomie.bib_taxref_rangs.id_rang", onupdate="CASCADE"), index=True
    )
    regne = DB.Column(DB.Unicode)
    phylum = DB.Column(DB.Unicode)
    classe = DB.Column(DB.Unicode)
    ordre = DB.Column(DB.Unicode)
    famille = DB.Column(DB.Unicode)
    sous_famille = DB.Column(DB.Unicode)
    tribu = DB.Column(DB.Unicode)
    cd_taxsup = DB.Column(DB.Integer)
    cd_sup = DB.Column(DB.Integer, index=True)
    cd_ref = DB.Column(DB.Integer, index=True)
    lb_nom = DB.Column(DB.Unicode)
    lb_auteur = DB.Column(DB.Unicode)
    nom_complet = DB.Column(DB.Unicode)
    nom_complet_html = DB.Column(DB.Unicode)
    nom_valide = DB.Column(DB.Unicode)
    nom_vern = DB.Column(DB.Unicode, index=True)
    nom_vern_eng = DB.Column(DB.Unicode)
    group1_inpn = DB.Column(DB.Unicode, index=True)
    group2_inpn = DB.Column(DB.Unicode, index=True)
    url = DB.Column(DB.Unicode)

    bib_taxref_habitat = relationship("BibTaxrefHabitat")
    bib_taxref_rang = relationship("BibTaxrefRang")
    bib_taxref_statut = relationship("BibTaxrefStatut")
    bib_listes = relationship("BibListe", secondary="taxonomie.cor_nom_liste")

    attributs = relationship(CorTaxonAttribut)
    medias = relationship(TMedia)


class TaxhubAdminLog(DB.Model):
    __tablename__ = "taxhub_admin_log"
    __table_args__ = {"schema": "taxonomie"}

    id = DB.Column(DB.Integer, primary_key=True)
    action_time = DB.Column(DB.DateTime, server_default=text("now()"))
    id_role = DB.Column(DB.Integer)
    object_type = DB.Column(DB.Unicode)
    object_id = DB.Column(DB.Integer)
    object_repr = DB.Column(DB.Unicode)
    change_type = DB.Column(DB.Unicode)
    change_message = DB.Column(DB.Unicode)


# /******************** A VOIR *********************************/

# class BibTaxrefCategoriesLr(DB.Model):
#     __tablename__ = 'bib_taxref_categories_lr'
#     __table_args__ = {'schema': 'taxonomie'}

#     id_categorie_france = DB.Column(CHAR(2), primary_key=True)
#     categorie_lr = DB.Column(DB.Unicode, nullable=False)
#     nom_categorie_lr = DB.Column(DB.Unicode), nullable=False)
#     desc_categorie_lr = DB.Column(DB.Unicode))

# class BibTaxrefStatut(DB.Model):
#     __tablename__ = 'bib_taxref_statuts'
#     __table_args__ = {'schema': 'taxonomie'}

#     id_statut = DB.Column(CHAR(1), primary_key=True)
#     nom_statut = DB.Column(DB.Unicode, nullable=False)


# t_taxref_bdc_statut = Table(
#     'taxref_bdc_statut', metadata,
#     DB.Column('cd_nom', DB.Integer, nullable=False),
#     DB.Column('cd_ref', DB.Integer, nullable=False),
#     DB.Column('cd_sup', DB.Integer),
#     DB.Column('cd_type_statut', DB.Unicode, nullable=False),
#     DB.Column('lb_type_statut', DB.Unicode),
#     DB.Column('regroupement_type', DB.Unicode),
#     DB.Column('code_statut', DB.Unicode),
#     DB.Column('label_statut', DB.Unicode0)),
#     DB.Column('rq_statut', Text),
#     DB.Column('cd_sig', DB.Unicode),
#     DB.Column('cd_doc', DB.Integer),
#     DB.Column('lb_nom', DB.Unicode0)),
#     DB.Column('lb_auteur', DB.Unicode0)),
#     DB.Column('nom_complet_html', DB.Unicode0)),
#     DB.Column('nom_valide_html', DB.Unicode0)),
#     DB.Column('regne', DB.Unicode),
#     DB.Column('phylum', DB.Unicode),
#     DB.Column('classe', DB.Unicode),
#     DB.Column('ordre', DB.Unicode),
#     DB.Column('famille', DB.Unicode),
#     DB.Column('group1_inpn', DB.Unicode),
#     DB.Column('group2_inpn', DB.Unicode),
#     DB.Column('lb_adm_tr', DB.Unicode),
#     DB.Column('niveau_admin', DB.Unicode),
#     DB.Column('cd_iso3166_1', DB.Unicode),
#     DB.Column('cd_iso3166_2', DB.Unicode),
#     DB.Column('full_citation', Text),
#     DB.Column('doc_url', Text),
#     DB.Column('thematique', DB.Unicode),
#     DB.Column('type_value', DB.Unicode),
#     schema='taxonomie'
# )


# class TaxrefBdcStatutType(DB.Model):
#     __tablename__ = 'taxref_bdc_statut_type'
#     __table_args__ = {'schema': 'taxonomie'}

#     cd_type_statut = DB.Column(DB.Unicode, primary_key=True)
#     lb_type_statut = DB.Column(DB.Unicode)
#     regroupement_type = DB.Column(DB.Unicode)
#     thematique = DB.Column(DB.Unicode)
#     type_value = DB.Column(DB.Unicode)


# class TaxrefProtectionArticle(DB.Model):
#     __tablename__ = 'taxref_protection_articles'
#     __table_args__ = {'schema': 'taxonomie'}

#     cd_protection = DB.Column(DB.Unicode, primary_key=True)
#     article = DB.Column(DB.Unicode))
#     intitule = DB.Column(Text)
#     arrete = DB.Column(Text)
#     cd_arrete = DB.Column(DB.Integer)
#     url_inpn = DB.Column(DB.Unicode))
#     cd_doc = DB.Column(DB.Integer)
#     url = DB.Column(DB.Unicode)
#     date_arrete = DB.Column(DB.Integer)
#     type_protection = DB.Column(DB.Unicode)
#     concerne_mon_territoire = DB.Column(Boolean)


# class TaxrefProtectionArticlesStructure(TaxrefProtectionArticle):
#     __tablename__ = 'taxref_protection_articles_structure'
#     __table_args__ = {'schema': 'taxonomie'}

#     cd_protection = DB.Column(ForeignKey('taxonomie.taxref_protection_articles.cd_protection'), primary_key=True)
#     alias_statut = DB.Column(DB.Unicode)
#     concerne_structure = DB.Column(Boolean)


# t_v_taxref_all_listes = Table(
#     'v_taxref_all_listes', metadata,
#     DB.Column('regne', DB.Unicode),
#     DB.Column('phylum', DB.Unicode),
#     DB.Column('classe', DB.Unicode),
#     DB.Column('ordre', DB.Unicode),
#     DB.Column('famille', DB.Unicode),
#     DB.Column('group1_inpn', DB.Unicode),
#     DB.Column('group2_inpn', DB.Unicode),
#     DB.Column('cd_nom', DB.Integer),
#     DB.Column('cd_ref', DB.Integer),
#     DB.Column('nom_complet', DB.Unicode),
#     DB.Column('nom_valide', DB.Unicode),
#     DB.Column('nom_vern', DB.Unicode0)),
#     DB.Column('lb_nom', DB.Unicode),
#     DB.Column('id_liste', DB.Integer),
#     schema='taxonomie'
# )


# t_vm_group1_inpn = Table(
#     'vm_group1_inpn', metadata,
#     DB.Column('group1_inpn', DB.Unicode, unique=True),
#     schema='taxonomie'
# )


# t_vm_group2_inpn = Table(
#     'vm_group2_inpn', metadata,
#     DB.Column('group2_inpn', DB.Unicode, unique=True),
#     schema='taxonomie'
# )


class VmTaxrefHierarchie(DB.Model):
    __tablename__ = "vm_taxref_hierarchie"
    __table_args__ = {"schema": "taxonomie"}

    regne = DB.Column(DB.Unicode)
    phylum = DB.Column(DB.Unicode)
    classe = DB.Column(DB.Unicode)
    ordre = DB.Column(DB.Unicode)
    famille = DB.Column(DB.Unicode)
    cd_nom = DB.Column(DB.Integer, primary_key=True)
    cd_ref = DB.Column(DB.Integer)
    lb_nom = DB.Column(DB.Unicode)
    id_rang = DB.Column(Text)
    nb_tx_fm = DB.Column(DB.Integer)
    nb_tx_or = DB.Column(DB.Integer)
    nb_tx_cl = DB.Column(DB.Integer)
    nb_tx_ph = DB.Column(DB.Integer)
    nb_tx_kd = DB.Column(DB.Integer)


# t_vm_taxref_list_forautocomplete = Table(
#     'vm_taxref_list_forautocomplete', metadata,
#     DB.Column('gid', BigDB.Integer, unique=True),
#     DB.Column('cd_nom', DB.Integer, index=True),
#     DB.Column('cd_ref', DB.Integer),
#     DB.Column('search_name', Text, index=True),
#     DB.Column('nom_valide', DB.Unicode),
#     DB.Column('lb_nom', DB.Unicode),
#     DB.Column('nom_vern', DB.Unicode0)),
#     DB.Column('regne', DB.Unicode),
#     DB.Column('group2_inpn', DB.Unicode),
#     schema='taxonomie',
#     comment='Vue matérialisée permettant de faire des autocomplete construite à partir d\'une requete sur tout taxref.'
# )


# class TaxrefListeRougeFr(DB.Model):
#     __tablename__ = 'taxref_liste_rouge_fr'
#     __table_args__ = {'schema': 'taxonomie'}

#     id_lr = DB.Column(DB.Integer, primary_key=True, server_default=text("nextval('taxonomie.taxref_liste_rouge_fr_id_lr_seq'::regclass)"))
#     ordre_statut = DB.Column(DB.Integer)
#     vide = DB.Column(DB.Unicode))
#     cd_nom = DB.Column(DB.Integer)
#     cd_ref = DB.Column(DB.Integer)
#     nomcite = DB.Column(DB.Unicode))
#     nom_scientifique = DB.Column(DB.Unicode))
#     auteur = DB.Column(DB.Unicode))
#     nom_vernaculaire = DB.Column(DB.Unicode))
#     nom_commun = DB.Column(DB.Unicode))
#     rang = DB.Column(CHAR(4))
#     famille = DB.Column(DB.Unicode)
#     endemisme = DB.Column(DB.Unicode))
#     population = DB.Column(DB.Unicode))
#     commentaire = DB.Column(Text)
#     id_categorie_france = DB.Column(ForeignKey('taxonomie.bib_taxref_categories_lr.id_categorie_france', onupdate='CASCADE'), nullable=False)
#     criteres_france = DB.Column(DB.Unicode))
#     liste_rouge = DB.Column(DB.Unicode))
#     fiche_espece = DB.Column(DB.Unicode))
#     tendance = DB.Column(DB.Unicode))
#     liste_rouge_source = DB.Column(DB.Unicode))
#     annee_publication = DB.Column(DB.Integer)
#     categorie_lr_europe = DB.Column(DB.Unicode
#     categorie_lr_mondiale = DB.Column(DB.Unicode

#     bib_taxref_categories_lr = relationship('BibTaxrefCategoriesLr')


# class TaxrefProtectionEspece(DB.Model):
#     __tablename__ = 'taxref_protection_especes'
#     __table_args__ = {'schema': 'taxonomie'}

#     cd_nom = DB.Column(ForeignKey('taxonomie.taxref.cd_nom', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
#     cd_protection = DB.Column(ForeignKey('taxonomie.taxref_protection_articles.cd_protection'), primary_key=True, nullable=False)
#     nom_cite = DB.Column(DB.Unicode))
#     syn_cite = DB.Column(DB.Unicode))
#     nom_francais_cite = DB.Column(DB.Unicode))
#     precisions = DB.Column(Text)
#     cd_nom_cite = DB.Column(DB.Unicode), primary_key=True, nullable=False)

#     taxref = relationship('Taxref')
#     taxref_protection_article = relationship('TaxrefProtectionArticle')
