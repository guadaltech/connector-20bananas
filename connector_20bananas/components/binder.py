from odoo.addons.component.core import Component


class BananasModelBinder(Component):
    _name = "bananas.binder"
    _inherit = ["base.binder", "base.bananas.component"]

    _external_field = "bananas_id"

    _apply_on = [
        "bananas.binding.res.partner",
        "bananas.binding.res.partner.pricelist",
        "bananas.binding.sale.order",
        "bananas.binding.product.product",
        "bananas.binding.product.pricelist",
        "bananas.binding.product.pricelist.item",
        "bananas.binding.product.blacklist",
        "bananas.binding.product.whitelist",
    ]
