from odoo import api, fields, models


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
