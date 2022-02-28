from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "order"

    state_tag_ids = fields.Many2many(
        "sale.order.line.tag", relation="line_ids", string="Line State"
    )
    order = fields.Integer(related="product_id.categ_id.sequence")
