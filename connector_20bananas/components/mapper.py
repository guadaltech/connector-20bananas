from odoo.addons.component.core import AbstractComponent


class BananasMapper(AbstractComponent):
    _name = "bananas.mapper"
    _inherit = ["base.import.mapper", "base.bananas.component"]

    def get_primary_key_attributes(self):
        """
        In this method, it is needed that you declare which pair of items
        are used to generate a unique key in the backend.
        """
        raise NotImplementedError()


class BananasImportMapper(AbstractComponent):
    _name = "bananas.import.mapper"
    _inherit = "bananas.mapper"
    _usage = "import.mapper"


class NavisionExporterMapper(AbstractComponent):
    _name = "bananas.exporter.mapper"
    _inherit = ["base.export.mapper", "base.bananas.component"]


class NavisionExportMapper(AbstractComponent):

    _name = "bananas.export.mapper"
    _inherit = "bananas.exporter.mapper"
    _usage = "export.mapper"
