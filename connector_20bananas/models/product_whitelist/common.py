from odoo import fields, models


class BananasBindingProductWhitelist(models.Model):
    _name = "bananas.binding.product.whitelist"
    _inherit = "bananas.binding.odoo"
    _inherits = {"product.whitelist": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="product.whitelist",
        string="Product Whitelist",
        required=True,
        ondelete="cascade",
    )
