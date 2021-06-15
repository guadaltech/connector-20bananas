from odoo import api, fields, models


class DeliverytDays(models.Model):
    _name = "delivery.days"
    _description = "Delivery Days"

    name = fields.Char(string="Day", compute="_compute_name")
    partner_ids = fields.Many2many(
        comodel_name="res.partner", inverse_name="delivery_days_ids", string="Clients"
    )
    dayofweek = fields.Selection(
        [
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        "Day of Week",
        required=True,
        index=True,
        default="0",
    )

    @api.depends("dayofweek")
    def _compute_name(self):
        for rec in self:
            days = [
                ("0", "Monday"),
                ("1", "Tuesday"),
                ("2", "Wednesday"),
                ("3", "Thursday"),
                ("4", "Friday"),
                ("5", "Saturday"),
                ("6", "Sunday"),
            ]
            name = days[int(rec.dayofweek)][1]
            rec.name = name


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_days_ids = fields.Many2many(
        comodel_name="delivery.days", string="Delivery Days", inverse_name="partner_ids"
    )


class BananasBindingResPartner(models.Model):
    _name = "bananas.binding.res.partner"
    _inherit = "bananas.binding.odoo"
    _inherits = {"res.partner": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="res.partner",
        string="Res Partner",
        required=True,
        ondelete="cascade",
    )

    # @job(default_channel='root.magento')
    @api.model
    def import_batch(self, backend, filters=None):
        """Prepare the import of records modified on Bananas
        For TEST purpose only!!!!
        """
        if filters is None:
            filters = {}
        with backend.work_on(self._name) as work:
            importer = work.component(usage="batch.importer")
            return importer.run(filters=filters)


class BananasBindingResPartnerPricelist(models.Model):
    _name = "bananas.binding.res.partner.pricelist"
    _inherit = "bananas.binding.res.partner"
