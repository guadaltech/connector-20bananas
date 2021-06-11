from odoo import api, fields, models


class BananasBinding(models.AbstractModel):
    _name = "bananas.binding"
    _inherit = "external.binding"
    _description = "Bananas Binding (abstract)"

    # 'odoo_id': openerp-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name="bananas.backend",
        string="Bananas Backend",
        required=True,
        ondelete="restrict",
    )

    bananas_id = fields.Text("ID on Bananas")

    sync_date = fields.Datetime(
        string="Sync Date", required=True, default=lambda _self: fields.Datetime.now()
    )


class BananasBindingOdoo(models.AbstractModel):
    _name = "bananas.binding.odoo"
    _inherit = "bananas.binding"
    _description = "Bananas Binding with Odoo binding (abstract)"

    def _get_selection(self):
        records = self.env["ir.model"].search([])
        return [(r.model, r.name) for r in records] + [("", "")]

    # 'odoo_id': odoo-side id must be re-declared in concrete model
    # for having a many2one instead of a reference field
    odoo_id = fields.Reference(
        required=True,
        ondelete="cascade",
        string="Odoo binding",
        selection=_get_selection,
    )

    _sql_constraints = [
        (
            "bananas_erp_uniq",
            "unique(backend_id, odoo_id)",
            "An ERP record with same ID already exists on Bananas.",
        ),
    ]
