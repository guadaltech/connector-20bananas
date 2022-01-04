from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    to_20bananas_bulto_1 = fields.Boolean(
        string="Unidades Bulto 1", help="Is the second unit in 20bananas"
    )

    to_20bananas_bulto_2 = fields.Boolean(
        string="Unidades Bulto 2", help="Is the third unit in 20bananas"
    )


class BananasBindingProductProduct(models.Model):
    _name = "bananas.binding.product.product"
    _inherit = "bananas.binding.odoo"
    _inherits = {"product.product": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
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


class ProductTemplate(models.Model):
    _inherit = "product.template"

    auto_export = fields.Boolean(
        string="Auto Export 20bananas", compute="_compute_auto_export", store=True
    )

    auto_export_selection = fields.Selection(
        string="Auto Export to 20Bananas ?",
        selection=[("yes", "Yes"), ("no", "No")],
    )

    bananas_product_bind_ids = fields.One2many(
        comodel_name="bananas.binding.product.product",
        inverse_name="odoo_id",
        string="Bananas Product Bindings",
    )

    def _get_active_backend_adapter(self):
        return self.env["bananas.backend"].search_count([]) > 0

    active_backend_adapter = fields.Boolean(
        compute="_compute_active_backend_adapter", default=_get_active_backend_adapter
    )

    def _compute_active_backend_adapter(self):
        self.active_backend_adapter = self.env["bananas.backend"].search_count([]) > 0

    @api.constrains("packaging_ids")
    def parent_required(self):
        packagin_bulto_1 = self.env["product.packaging"].search_count(
            [("product_id", "=", self.id), ("to_20bananas_bulto_1", "=", True)]
        )
        if packagin_bulto_1 > 1:
            raise ValidationError(
                _(
                    "Solo puede haber un paquete como unidad de bulto 1 "
                    "para ser exportado a 20bananas"
                )
            )
        packagin_bulto_2 = self.env["product.packaging"].search_count(
            [("product_id", "=", self.id), ("to_20bananas_bulto_2", "=", True)]
        )
        if packagin_bulto_2 > 1:
            raise ValidationError(
                _(
                    "Solo puede haber un paquete como unidad de bulto 2 "
                    "para ser exportado a 20bananas"
                )
            )

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
        with backend_id.work_on("bananas.binding.product.product") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self.product_variant_id)

    # metodo para la acción de servidor para exportar los productos seleccionadas
    def action_export(self):
        for rec in self:
            rec.button_to_export_bananas()

        # accion del cron

    def cron_export_product_bananas(self):
        models = self.env["product.template"].search([("auto_export", "=", True)])
        for model in models:
            model.acction_export()


class ProductProduct(models.Model):
    _inherit = "product.product"

    auto_export = fields.Boolean(
        string="Auto Export 20bananas", compute="_compute_auto_export", store=True
    )

    auto_export_selection = fields.Selection(
        string="Auto Export to 20Bananas ?",
        selection=[("yes", "Yes"), ("no", "No")],
    )

    bananas_product_bind_ids = fields.One2many(
        comodel_name="bananas.binding.product.product",
        inverse_name="odoo_id",
        string="Bananas Product Bindings",
    )

    def _get_active_backend_adapter(self):
        return self.env["bananas.backend"].search_count([]) > 0

    active_backend_adapter = fields.Boolean(
        compute="_compute_active_backend_adapter", default=_get_active_backend_adapter
    )

    def _compute_active_backend_adapter(self):
        self.active_backend_adapter = self.env["bananas.backend"].search_count([]) > 0

    @api.constrains("packaging_ids")
    def parent_required(self):
        packagin_bulto_1 = self.env["product.packaging"].search_count(
            [("product_id", "=", self.id), ("to_20bananas_bulto_1", "=", True)]
        )
        if packagin_bulto_1 > 1:
            raise ValidationError(
                _(
                    "Solo puede haber un paquete como unidad de bulto 1 "
                    "para ser exportado a 20bananas"
                )
            )
        packagin_bulto_2 = self.env["product.packaging"].search_count(
            [("product_id", "=", self.id), ("to_20bananas_bulto_2", "=", True)]
        )
        if packagin_bulto_2 > 1:
            raise ValidationError(
                _(
                    "Solo puede haber un paquete como unidad de bulto 2 "
                    "para ser exportado a 20bananas"
                )
            )

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
        with backend_id.work_on("bananas.binding.product.product") as backend:
            record_exporter = backend.component(usage="record.exporter")
            record_exporter.run(self.product_variant_id)

    # metodo para la acción de servidor para exportar los productos seleccionadas
    def action_export(self):
        for rec in self:
            rec.button_to_export_bananas()

        # accion del cron

    def cron_export_product_bananas(self):
        models = self.env["product.template"].search([("auto_export", "=", True)])
        for model in models:
            model.acction_export()
