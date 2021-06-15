from logging import getLogger

from odoo import _, fields, models
from odoo.odoo.exceptions import UserError

_logger = getLogger(__name__)


class BananasConnectorBackend(models.Model):
    _name = "bananas.backend"
    _inherit = "connector.backend"
    _description = "Bananas Connector Backend"
    _usage = "backend"

    # Basic Information for the connection
    url = fields.Char(
        string="Bananas URL endpoint",
        help="The URL base where the service is.",
        reuired=True,
    )
    api_key = fields.Char(
        string="API KEY for the api of Bananas",
        help="The API KEY that you obtain for make requets to api.",
        required=True,
    )

    # Agrego las Terminaciones de la api para cada uno de los endpoint de la Api
    endpoint_clients = fields.Char(string="Endpoint for Clients")
    endpoint_products = fields.Char(string="Endpoint for Products")
    endpoint_order_sale = fields.Char(string="Enpoint for order sale")
    date_of_order_sale = fields.Char(
        string="Date for the order sale", help="The format is YYYY-mm-dd"
    )
    endpoint_product_pricelist = fields.Char(string="Endpoint for the rate")
    endpoint_product_pricelist_item = fields.Char(
        string="Endpoint for produt with rate"
    )
    endpoint_product_pricelist_client = fields.Char(
        string="Endpoint for asociate rate to client"
    )

    # Este es el metodo usado para importar los clientes
    def import_customers(self):
        # TODO Implement call to import parnters
        for backend in self:
            if not backend.endpoint_clients:
                raise UserError(
                    _("Before import the clients please, introduce the endpoint")
                )
            self.env["bananas.binding.res.partner"].import_batch(backend)
        return True

    # Este es el metodo usado para importar los productos
    def import_products(self):
        for backend in self:
            if not backend.endpoint_products:
                raise UserError(
                    _("Before import the product please, introduce the endpoint")
                )
            self.env["bananas.binding.product.product"].import_batch(backend)

    # Este es el metodo usado para importar los pedidos
    def import_orders(self):
        for backend in self:
            if not backend.endpoint_order_sale:
                raise UserError(
                    _("Before import the order sale please, introduce the endpoint")
                )
            self.env["bananas.binding.sale.order"].import_batch(backend)

    # Este es el metodo usado para importar tarifas(es decir crea los pricelist)
    def import_rates(self):
        for backend in self:
            if not backend.endpoint_product_pricelist:
                raise UserError(
                    _("Before import the rate for price please, introduce the endpoint")
                )
            self.env["bananas.binding.product.pricelist"].import_batch(backend)

    # Este es el metodo usado para agregarle a las tarifas los precios
    # de los productos(pricelist.item)
    def import_rates_item(self):
        for backend in self:
            if not backend.endpoint_product_pricelist_item:
                raise UserError(
                    _(
                        "Before import the rate for price item please, "
                        "introduce the endpoint"
                    )
                )
            self.env["bananas.binding.product.pricelist.item"].import_batch(backend)

    # Este es el metodo usado para afregarle a los clientes las
    # tarifas(aun no esta funcioando correctamete)
    def import_rates_client(self):
        for backend in self:
            if not backend.endpoint_product_pricelist_client:
                raise UserError(
                    _(
                        "Before asociate the clients with his rates, "
                        "introduce the endpoint"
                    )
                )
            self.env["bananas.binding.res.partner.pricelist"].import_batch(backend)

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones de CLientes
    def cron_import_clients(self):
        return {
            "name": _("Create Cron Client"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_customers()",
            },
        }

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones de Product
    def cron_import_products(self):
        return {
            "name": _("Create Cron Product"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_products()",
            },
        }

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones de Orders
    def cron_import_orders(self):
        return {
            "name": _("Create Cron Orders"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_orders()",
            },
        }

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones de Rates
    def cron_import_rates(self):
        return {
            "name": _("Create Cron Rates"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_rates()",
            },
        }

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones de Rate Items
    def cron_import_rates_item(self):
        return {
            "name": _("Create Cron Rate Items"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_rates_item()",
            },
        }

    # Este es un metodo para llamar al wizar y crear un cron para
    # automatizar las importaciones Rates for CLientes
    def cron_import_rates_client(self):
        return {
            "name": _("Create Cron Rates forClient"),
            "view_mode": "form",
            "res_model": "wizard.cron.bananas.conector",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_model_id": self.id,
                "default_type_import": "import_rates_client()",
            },
        }

    # Este ina a ser usado para marcar un pedido como servido
    # pero se ha colocado en otro sitio por el momento
    # def marck_sale_as_served(self):
    #     for backend in self:
    #         if not backend.endpoint_order_sale:
    #             raise UserError(
    #                 "Before marck sale as served, please introduce
    #                 the enpoint for sale"
    #             )
    #         self.env["bananas.binding.sale.order"].marck_as_served(backend)
