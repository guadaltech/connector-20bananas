from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductPricelistBatchImporter(Component):
    """Import the Bananas Partners.
    For every partner in the list, a delayed job is created.
    """

    _name = "bananas.product.pricelist.batch.importer"
    _inherit = "bananas.batch.importer"
    _apply_on = "bananas.binding.product.pricelist"


class ProducPricelistMapper(Component):
    _name = "bananas.product.pricelist.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = "bananas.binding.product.pricelist"

    def get_primary_key_attributes(self):
        """
        This method is used to declare the "external_id" used for this object
        (in this case, a res.partner)
        """

        return ["codtarifa"]

    direct = [
        ("descripcion", "name"),
    ]


class ProductPricelistItemBatchImporter(Component):
    """Import the Bananas Partners.
    For every partner in the list, a delayed job is created.
    """

    _name = "bananas.product.pricelist.item.batch.importer"
    _inherit = "bananas.batch.importer"
    _apply_on = "bananas.binding.product.pricelist.item"


class ProducPricelistItemMapper(Component):
    _name = "bananas.product.pricelist.item.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = "bananas.binding.product.pricelist.item"

    def get_primary_key_attributes(self):
        """
        This method is used to declare the "external_id" used for this object
        (in this case, a res.partner)
        """

        return ["referencia", "codtarifa"]

    direct = [("precio", "fixed_price")]

    @mapping
    def compute_compute_fixed(self, record):
        return {"compute_price": "fixed"}

    @mapping
    def compoute_product_tmpl_id(self, record):
        product = self.env["bananas.binding.product.product"].search(
            [("bananas_id", "=", record["referencia"])]
        )
        return {"product_tmpl_id": product.odoo_id.id}

    @mapping
    def compute_base_pricelist_id(self, record):
        pricelist = self.env["bananas.binding.product.pricelist"].search(
            [("bananas_id", "=", record["codtarifa"])]
        )
        return {"pricelist_id": pricelist.odoo_id.id}

    @mapping
    def compute_applied_on(self, record):
        return {"applied_on": "1_product"}
