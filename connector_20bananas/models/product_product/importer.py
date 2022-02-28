import base64

from logging import getLogger

import requests

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

_logger = getLogger(__name__)


class ProductProductBatchImporter(Component):
    """Import the Bananas Partners.
    For every partner in the list, a delayed job is created.
    """

    _name = "bananas.product.product.batch.importer"
    _inherit = "bananas.batch.importer"
    _apply_on = "bananas.binding.product.product"


class ProductProductMapper(Component):
    _name = "bananas.product.product.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = "bananas.binding.product.product"

    def get_primary_key_attributes(self):
        """
        This method is used to declare the "external_id" used for this object
        (in this case, a res.partner)
        """

        return ["referencia"]

    direct = [
        ("nombre", "name"),
        ("activo", "sale_ok"),
        ("descripcion", "description"),
        ("precio", "lst_price"),
        ("codigosbarra", "barcode"),
    ]

    @mapping
    def compute_category_id(self, record):
        if "familia" in record:
            catg_id_father = self.env["product.category"].search(
                [("name", "=", record["familia"])], limit=1
            )
            if not catg_id_father:
                catg_id_father = self.env["product.category"].create(
                    {"name": record["familia"]}
                )
            cat_id = self.env["product.category"].search(
                [("name", "=", record["subfamilia"])], limit=1
            )
            if not cat_id:
                cat_id = self.env["product.category"].create(
                    {"name": record["subfamilia"], "parent_id": catg_id_father.id}
                )
            return {"categ_id": cat_id.id}

    # Tengo de darle alguna vuelta más a esto de las unidades
    # En principio solo voy a colocar las unidades de medida
    @mapping
    def compute_uom_id(self, record):
        # Vamas a buscar y crear las unidades de medida relacionada con el producto,
        # en caso de que no exista ya en el sistema
        uom_cat_id = self.env["uom.category"].search([("name", "=", "Unit")], limit=1)
        uom_id = self.env["uom.uom"].search([("name", "=", record["unidad"])], limit=1)
        if not uom_id:
            # escojo la categoria de unidad en principio
            uom_id = self.env["uom.uom"].search(
                [("category_id", "=", uom_cat_id.id), ("uom_type", "=", "reference")]
            )
            if uom_id:
                # Cambiamos el nombre en principio para que sea nuestra referencia
                uom_id.write({"name": record["unidad"]})
        return {"uom_id": uom_id.id}

    @mapping
    def compute_packaging_ids(self, record):
        packaging_ids = []
        _logger.info("Esta es la catidad " + record["unidadesxbulto"])
        if (
            "unidadbulto" in record
            and "unidadesxbulto" in record
            and record["vendobulto"] == "1"
            and record["unidadesxbulto"] != "0.0"
        ):
            producto = self.env["bananas.binding.product.product"].search(
                [("bananas_id", "=", record["referencia"])]
            )
            if producto:
                package = self.env["product.packaging"].search(
                    [
                        ("name", "=", record["unidadbulto"]),
                        ("product_id", "=", producto.odoo_id.id),
                    ]
                )
                _logger.info("Esta es la catidad " + record["unidadesxbulto"])
                if not package and not record["unidadesxbulto"] == "0.0":
                        package = self.env["product.packaging"].create(
                            {
                                "name": record["unidadbulto"],
                                "product_id": producto.odoo_id.id,
                                "qty": record["unidadesxbulto"],
                            }
                        )
                        packaging_ids.append(package.id)
        _logger.info("Esta es la catidad " + record["unidadesxbulto2"])
        if (
            "unidadbulto2" in record
            and "unidadesxbulto2" in record
            and record["vendobulto2"] == "1"
            and record["unidadesxbulto2"] != "0.0"
        ):
            producto = self.env["bananas.binding.product.product"].search(
                [("bananas_id", "=", record["referencia"])]
            )
            if producto:
                package = self.env["product.packaging"].search(
                    [
                        ("name", "=", record["unidadbulto2"]),
                        ("product_id", "=", producto.odoo_id.id),
                    ]
                )
                _logger.info("Esta es la catidad " + record["unidadesxbulto2"])
                if not package and not record["unidadesxbulto2"] == "0.0":
                        package = self.env["product.packaging"].create(
                            {
                                "name": record["unidadbulto2"],
                                "product_id": producto.odoo_id.id,
                                "qty": record["unidadesxbulto2"],
                            }
                        )
                        packaging_ids.append(package.id)

            return {"packaging_ids": packaging_ids}

    @mapping
    def compute_image_1920(self, record):
        try:
            aux = requests.get(record["foto"], headers={"Content-Type": "image/jpeg"})
            image = base64.b64encode(aux.content)
        except ValueError:
            image = False
        return {"image_1920": image}
