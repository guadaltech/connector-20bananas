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
            return importer.run(filters=filters)
