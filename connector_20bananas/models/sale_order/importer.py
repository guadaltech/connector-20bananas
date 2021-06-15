from datetime import datetime

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class SaleOrderBatchImporter(Component):
    """Import the Bananas Sale Order.
    For every partner in the list, a delayed job is created.
    """

    _name = "bananas.sale.order.batch.importer"
    _inherit = "bananas.batch.importer"
    _apply_on = "bananas.binding.sale.order"


class SaleOrderMapper(Component):
    _name = "bananas.sale.order.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = "bananas.binding.sale.order"

    def get_primary_key_attributes(self):
        """
        This method is used to declare the "external_id" used for this object
        (in this case, a res.partner)
        """
        return ["idpedido"]

    def _get_sale_order_lines(self, record):
        pedido = self.env["bananas.binding.sale.order"].search(
            [("bananas_id", "=", record["idpedido"])]
        )
        if pedido:
            return ""
        else:
            return "productos"

    @mapping
    def compute_user_id(self, record):
        if "codcomercial" in record and record["codcomercial"]:
            user = self.env["bananas.binding.res.partner"].search(
                [("bananas_id", "=", record["codcomercial"])]
            )
            if not user:
                user_id = self.env.user
            else:
                user_id = self.env["res.user"].search(
                    [("partner_id", "=", user.odoo_id.id)]
                )
        else:
            user_id = self.env.user
        return {"user_id": user_id.id}

    @mapping
    def compute_partner_id(self, record):
        client = self.env["bananas.binding.res.partner"].search(
            [("bananas_id", "=", record["codcliente"])]
        )
        if client:
            return {"partner_id": client.odoo_id.id}
        else:
            client = self.env["res.partner"].search(
                [("name", "=", record["nombrecliente"])]
            )
            if not client:
                raise UserError(
                    _("The client  hasn't been importer, pleas import before continue")
                )
            return {"partner_id": client.id}

    @mapping
    def compute_date_order(self, record):
        date = record["fecha"] + " " + record["hora"]
        date_order = datetime.strptime(date, "%Y-%m-%d %H:%M")
        return {"date_order": date_order}

    @mapping
    def compute_state(self, record):
        if record["servido10"] == "1":
            return {"state": "sale"}

    children = [(_get_sale_order_lines, "order_line", "sale.order.line")]

    def _map_child(self, map_record, from_attr, to_attr, model_name):
        assert self._map_child_usage is not None, "_map_child_usage required"
        if callable(from_attr):
            from_attr = from_attr(self, map_record.source)
        child_records = map_record.source[from_attr]
        mapper_child = self._get_map_child_component(model_name)
        items = mapper_child.get_items(
            child_records, map_record, to_attr, options=self.options
        )
        return items


class SaleOrderLineMapper(Component):
    _name = "bananas.sale.order.line.mapper"
    _inherit = "bananas.import.mapper"
    _apply_on = "sale.order.line"

    @mapping
    def compute_product_uom_qty(self, record):
        product = self.env["bananas.binding.product.product"].search(
            [("bananas_id", "=", record["referencia"])]
        )
        if not product:
            raise UserError(
                _("The product hasn't been importer, pleas import before continue")
            )
        packages = self.env["product.packaging"].search(
            [("name", "=", record["unidad"]), ("product_id", "=", product.odoo_id.id)]
        )
        if packages:
            return {"product_uom_qty": int(record["cantidad"]) * packages.qty}
        else:
            return {"product_uom_qty": int(record["cantidad"])}

    @mapping
    def compute_price_unit(self, record):
        product = self.env["bananas.binding.product.product"].search(
            [("bananas_id", "=", record["referencia"])]
        )
        if not product:
            raise UserError(
                _("The product hasn't been importer, pleas import before continue")
            )
        packages = self.env["product.packaging"].search(
            [("name", "=", record["unidad"]), ("product_id", "=", product.odoo_id.id)]
        )
        if packages:
            return {"price_unit": int(record["precio"]) / packages.qty}
        else:
            return {"product_uom_qty": int(record["precio"])}

    @mapping
    def compute_name(self, record):
        if "observaciones" in record and record["observaciones"]:
            name = record["observaciones"]
        else:
            name = record["nombre"]
        return {"name": name}

    @mapping
    def compute_product_id(self, record):
        product = self.env["bananas.binding.product.product"].search(
            [("bananas_id", "=", record["referencia"])]
        )
        if not product:
            raise UserError(
                _(
                    "The product hasn't been importer, please before import the order,"
                    " import all products."
                )
            )
        return {"product_id": product.odoo_id.id}

    @mapping
    def compute_product_uom(self, record):
        unidad = self.env["uom.uom"].search([("name", "=", record["unidad"])])
        if not unidad:
            product = self.env["bananas.binding.product.product"].search(
                [("bananas_id", "=", record["referencia"])]
            )
            if not product:
                raise UserError(
                    _("The product hasn't been importer, pleas import before continue")
                )
            packages = self.env["product.packaging"].search(
                [
                    ("name", "=", record["unidad"]),
                    ("product_id", "=", product.odoo_id.id),
                ]
            )
            if not packages:
                raise UserError(
                    (
                        _(
                            "We can't create the order line because "
                            "the unit for the line doesn't exit or"
                            " threre aren't a packaging wyhs these name, "
                            "pleas befere retray it, create the %s unit or the package"
                        )
                    )
                    % (record["unidad"])
                )
            return {"product_uom": product.uom_id.id, "product_packaging": packages.id}
        return {"product_uom": unidad.id}
