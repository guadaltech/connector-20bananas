from odoo import api, fields, models


class BananasBindingProductPricelist(models.Model):
    _name = "bananas.binding.product.pricelist"
    _inherit = "bananas.binding.odoo"
    _inherits = {"product.pricelist": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Product Pricelist",
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


class BananasBindingProductPricelistItem(models.Model):
    _name = "bananas.binding.product.pricelist.item"
    _inherit = "bananas.binding.odoo"
    _inherits = {"product.pricelist.item": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="product.pricelist.item",
        string="Product Pricelist Item",
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
            return importer.with_delay().run(filters=filters)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    auto_export = fields.Boolean(
        string="Auto Export 20bananas", compute="_compute_auto_export", store=True
    )

    auto_export_selection = fields.Selection(
        string="Auto Export to 20Bananas ?",
        selection=[("yes", "Yes"), ("no", "No")],
    )

    bananas_pricelist_bind_ids = fields.One2many(
        comodel_name="bananas.binding.product.pricelist",
        inverse_name="odoo_id",
        string="Bananas Pricelist Bindings",
    )

    bananas_pricelist_item_bind_ids = fields.One2many(
        comodel_name="bananas.binding.product.pricelist.item",
        inverse_name="pricelist_id",
        string="Bananas Pricelist Bindings",
    )

    def _get_active_backend_adapter(self):
        return self.env["bananas.backend"].search_count([]) > 0

    active_backend_adapter = fields.Boolean(
        compute="_compute_active_backend_adapter", default=_get_active_backend_adapter
    )

    def _compute_active_backend_adapter(self):
        self.active_backend_adapter = self.env["bananas.backend"].search_count([]) > 0

    @api.depends("auto_export_selection")
    def _compute_auto_export(self):
        for rec in self:
            if rec.auto_export_selection == "yes":
                rec.auto_export = True
            else:
                rec.auto_export = False

    # creamos un metodo para exportar los productos para las pruebas
    def button_to_export_bananas(self):
        backend_id = self.env["bananas.backend"].search([])
        with backend_id.work_on("bananas.binding.product.pricelist") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self)

    def button_to_export_rate_item_bananas(self):
        for item in self.item_ids:
            item.button_to_export_bananas()

    def button_to_export_pricelist_bananas(self):
        backend_id = self.env["bananas.backend"].search([])
        with backend_id.work_on("bananas.binding.res.partner.pricelist") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self)

    # metodo para la acción de servidor para exportar las tarifas seleccionadas
    def action_export(self):
        for rec in self:
            rec.button_to_export_bananas()
            rec.button_to_export_rate_item_bananas()

    # accion del cron
    def cron_export_product_rate_bananas(self):
        models = self.env["product.pricelist"].search([("auto_export", "=", True)])
        for model in models:
            model.with_delay().acction_export()


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    # creamos un metodo para exportar los productos para las pruebas
    def button_to_export_bananas(self):
        backend_id = self.env["bananas.backend"].search([])
        with backend_id.work_on("bananas.binding.product.pricelist.item") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self)
