from odoo import fields, models


class BananasBindingProductBlacklist(models.Model):
    _name = "bananas.binding.product.blacklist"
    _inherit = "bananas.binding.odoo"
    _inherits = {"product.blacklist": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="product.blacklist",
        string="Product Blacklist",
        required=True,
        ondelete="cascade",
    )
