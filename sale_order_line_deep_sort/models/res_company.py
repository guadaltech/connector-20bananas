# Copyright 2018 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import fields, models

SORTING_CRITERIA = [
    ("name", "By name"),
    ("product_id.name", "By product name"),
    ("product_id.default_code", "By product reference"),
    ("date_planned", "By date planned"),
    ("price_unit", "By price"),
    ("product_qty", "By quantity"),
    ("product_id.categ_id.sequence", "By product category")
]

SORTING_DIRECTION = [
    ("asc", "Ascending"),
    ("desc", "Descending"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    default_so_line_order = fields.Selection(
        selection=SORTING_CRITERIA,
        string="Line Order",
        help="Select a sorting criteria for sale order lines.",
    )
    default_so_line_direction = fields.Selection(
        selection=SORTING_DIRECTION,
        string="Sort Direction",
        help="Select a sorting direction for sale order lines.",
    )
