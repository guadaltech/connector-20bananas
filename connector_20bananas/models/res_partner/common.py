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

    auto_export = fields.Boolean(
        string="Auto Export 20bananas", compute="_compute_auto_export", store=True
    )

    auto_export_selection = fields.Selection(
        string="Auto Export to 20Bananas ?",
        selection=[("yes", "Yes"), ("no", "No")],
    )

    bananas_customer_bind_ids = fields.One2many(
        comodel_name="bananas.binding.res.partner",
        inverse_name="odoo_id",
        string="Bananas Customer Bindings",
    )

    def _get_active_backend_adapter(self):
        return self.env["bananas.backend"].search_count([]) > 0

    active_backend_adapter = fields.Boolean(
        compute="_compute_active_backend_adapter", default=_get_active_backend_adapter
    )

    def _compute_active_backend_adapter(self):
        self.active_backend_adapter = self.env["bananas.backend"].search_count([]) > 0

    def button_to_export_bananas(self):
        backend_id = self.env["bananas.backend"].search([])
        with backend_id.work_on("bananas.binding.res.partner") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self)

    def button_to_export_pricelist_bananas(self):
        backend_id = self.env["bananas.backend"].search([])
        with backend_id.work_on("bananas.binding.res.partner.pricelist") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self)

    @api.depends("auto_export_selection")
    def _compute_auto_export(self):
        for rec in self:
            if rec.auto_export_selection == "yes":
                rec.auto_export = True
            else:
                rec.auto_export = False

    # Accion del cron
    def cron_export_clients_bananas(self):
        models = self.env["res.partner"].search([("auto_export", "=", True)])
        for model in models:
            model.action_export()

    def cron_export_clients_rate_bananas(self):
        models = self.env["res.partner"].search([("auto_export", "=", True)])
        for model in models:
            model.with_delay().action_export_rate_client()

    # metodo para la acción de servidor para exportar los clientes seleccionadas
    def action_export(self):
        for rec in self:
            rec.button_to_export_bananas()

    def action_export_rate_client(self):
        for rec in self:
            rec.with_delay().button_to_export_pricelist_bananas()


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
