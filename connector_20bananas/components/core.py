from odoo.addons.component.core import AbstractComponent


class BananasConnectorComponent(AbstractComponent):
    _name = "base.bananas.component"
    _inherit = "base.connector"
    _collection = "bananas.backend"
