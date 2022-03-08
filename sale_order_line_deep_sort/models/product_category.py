from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    _order = "sequence"

    sequence = fields.Integer(
        help="Gives the sequence order when displaying a list of product categories.",
        index=True,
    )
