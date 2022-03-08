from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    state_tag_ids = fields.Many2many(
        "sale.order.line.tag", relation="line_ids", string="Line State"
    )
