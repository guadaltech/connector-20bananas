from odoo.odoo.exceptions import UserError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ResPartnerVendorBatchImporter(Component):
    """Import the Bananas Partners.
    For every partner in the list, a delayed job is created.
    """

    _name = "bananas.res.partner.batch.importer"
    _inherit = "bananas.batch.importer"
    _apply_on = ["bananas.binding.res.partner", "bananas.binding.res.partner.pricelist"]


class ResPartnerMapper(Component):
    _name = "bananas.res.partner.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = ["bananas.binding.res.partner", "bananas.binding.res.partner.pricelist"]

    def get_primary_key_attributes(self):
        """
        This method is used to declare the "external_id" used for this object
        (in this case, a res.partner)
        """
        return ["codcliente"]

    direct = [
        ("nombrecliente", "name"),
    ]

    @mapping
    def compute_user_id(self, record):
        if "codcomercial":
            user_id = self.env["bananas.binding.res.partner"].search(
                [("bananas_id", "=", record["codcomercial"])]
            )
            if user_id:
                return {"user:is": user_id}

    @mapping
    def compute_delivery_days_ids(self, record):
        if "diasreparto" in record:
            dias = []
            count = 0
            for i in record["diasreparto"]:
                if i == "1":
                    dias.append(count)
                count += 1
            return {"delivery_days_ids": dias}

    @mapping
    def compute_property_product_pricelist(self, record):
        if "codtarifa" in record:
            cliente = self.env["bananas.binding.res.partner"].search(
                [("bananas_id", "=", record["codcliente"])]
            )
            if not cliente:
                raise UserError("Before asociate the rate to a cliente, import clients")
            tarifa = self.env["bananas.binding.product.pricelist"].search(
                [("bananas_id", "=", record["codtarifa"])]
            )
            if not tarifa:
                raise UserError("Before asociate the rate to a cliente, import rates")
            tarifa_odoo = tarifa.odoo_id
            aux = cliente.odoo_id.sudo().write(
                {"property_product_pricelist": tarifa_odoo}
            )
            return {"property_product_pricelist", tarifa_odoo.id}
