from odoo import api, fields, models


class ConnectionBananasCron(models.Model):
    _name = "connections.bananas.cron"
    _description = "Cron Trigger"

    cron_id = fields.Many2one(
        "ir.cron", delegate=True, required=True, ondelete="cascade"
    )

    backend_id = fields.Many2one("bananas.backend", required="True")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault("name", vals.get("trigger_name", "Sync"))
        return super(ConnectionBananasCron, self).create(vals_list)

    def method_direct_trigger(self):
        res = self.cron_id.method_direct_trigger()
        return res
