from random import randint

from odoo import fields, models


class SaleOrderLineTag(models.Model):
    _name = "sale.order.line.tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char("Tag Name", required=True, translate=True)
    color = fields.Integer(default=_get_default_color)
    line_ids = fields.Many2many("sale.order.line")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists !"),
    ]
