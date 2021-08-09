from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductPricelistExporter(Component):
    _name = "bananas.product.pricelist.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.product.pricelist"]


class ProductPricelistExporterMapper(Component):
    _name = "bananas.product.pricelist.exporter.mapper"
    _inherit = "bananas.export.mapper"
    _apply_on = "bananas.binding.product.pricelist"

    @mapping
    def compute_codtarifa(self, record):
        if record["bananas_id"]:
            return {"codtarifa": record["bananas_id"]}
        else:
            # aqui va el calculo con la secuencia
            referencia = (
                self.env["ir.sequence"].next_by_code("bananas.product.pricelist") or ""
            )
            return {"codtarifa": referencia}

    @mapping
    def compute_descripcion(self, record):
        return {"descripcion": record["name"]}


class ProductPricelistItemExporter(Component):
    _name = "bananas.product.pricelist.item.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.product.pricelist.item"]


class ProductPricelistItemExporterMapper(Component):
    _name = "bananas.product.pricelist.item.exporter.mapper"
    _inherit = "bananas.export.mapper"
    _apply_on = "bananas.binding.product.pricelist.item"

    @mapping
    def compute_codtarifa(self, record):
        tarifa = record["pricelist_id"]
        tarifa_binding = self.env["bananas.binding.product.pricelist"].search(
            [("odoo_id", "=", tarifa.id)]
        )
        if tarifa_binding and tarifa_binding.bananas_id:
            return {"codtarifa": tarifa_binding.bananas_id}
        else:
            raise ValidationError(
                _(
                    "The Rate is no exported to 20bananas, "
                    "so we can't add the product item to the rate"
                )
            )

    @mapping
    def compute_referencia(self, record):
        product = record["product_tmpl_id"]
        product_binding = self.env["bananas.binding.product.product"].search(
            [("odoo_id", "=", product.id)]
        )
        if product_binding and product_binding.bananas_id:
            return {"referencia": product_binding.bananas_id}
        else:
            raise ValidationError(
                _(
                    "The Product is no exported to 20bananas, "
                    "so we can't add the product item to the rate"
                )
            )

    @mapping
    def compute_price(self, record):
        return {"precio": record["fixed_price"]}
