from odoo import api, fields, models


class BananasBindingSaleOrder(models.Model):
    _name = "bananas.binding.sale.order"
    _inherit = "bananas.binding.odoo"
    _inherits = {"sale.order": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def button_marck_as_servide_in_bananas(self):
        for record in self:
            backend_id = self.env["bananas.backend"].search([])
            with backend_id.work_on("bananas.binding.sale.order") as backend:
                record_exporter = backend.component(usage="record.exporter")
                record_exporter.run(self)
