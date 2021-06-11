import json
from logging import getLogger

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.component.core import Component

_logger = getLogger(__name__)

##El backenAdapter abstrae del backen, que tiene la informacion necesaria para la conexion con la api,
##dicha informacion para generar un metodo que conecta con los endpoint de la api.


class BananasBackendAdapter:
    def __init__(self, full_url, api_key, endpoint):
        self.location = full_url
        self.api_key = api_key
        self.endpoint = endpoint

    def connect(self, type, id, playload):
        if not playload:
            headers = {"apikey": self.api_key}
        else:
            headers = {"apikey": self.api_key, "Content-type": "aplicatio/json"}
            playload = json.dumps([playload])
        if id:
            return requests.request(
                type, self.location + self.endpoint + id, headers=headers, data=playload
            )
        else:
            return requests.request(
                type, self.location + self.endpoint, headers=headers, data=playload
            )


class BananasCRUDAdapter(Component):
    _name = "bananas.crud.adapter"
    _inherit = ["base.backend.adapter", "base.bananas.component"]
    _usage = "backend.adapter"

    def __init__(self, environment):
        super(Component, self).__init__(environment)

        if not environment.collection:
            raise AttributeError("No backend found for this adapter!")
        if not hasattr(environment, "model"):
            raise AttributeError("No model found for this adapter!")

        self.backend = environment.collection
        _logger.info(
            "Started Backend Service for {model}".format(model=environment.model._name)
        )
        ##Se asigna el endpoint en función de el modelo que se este usando.
        if environment.model._name == "bananas.binding.res.partner":
            endpoint = self.backend.endpoint_clients
        if environment.model._name == "bananas.binding.res.partner.pricelist":
            endpoint = self.backend.endpoint_product_pricelist_client
        if environment.model._name == "bananas.binding.product.product":
            endpoint = self.backend.endpoint_products
        if environment.model._name == "bananas.binding.sale.order":
            if self.backend.date_of_order_sale:
                endpoint = (
                    self.backend.endpoint_order_sale + self.backend.date_of_order_sale
                )
            else:
                endpoint = self.backend.endpoint_order_sale
        if environment.model._name == "bananas.binding.product.pricelist":
            endpoint = self.backend.endpoint_product_pricelist
        if environment.model._name == "bananas.binding.product.pricelist.item":
            endpoint = self.backend.endpoint_product_pricelist_item

        self.api = BananasBackendAdapter(
            self.backend.url, self.backend.api_key, endpoint
        )

    # Se crean los metodos crud necesarios
    def search(self, filters=[None], attributes=dict()):
        response = self.api.connect("GET", "", {})

        _logger.debug(
            "Requested ReadMultiple with filters {filters} and attributes"
            " {attributes}".format(filters=filters, attributes=attributes)
        )

        res = response.json()
        if res["response"] == "ERROR":
            raise UserError(
                "We have get an error has a response in the request to the api, "
                "these is the error ('%s'), please check it before retry it"
                % (res["description"])
            )
        data = res["records"]
        return data

    def search_read(self, filters=[None], attributes=dict()):
        return self.search(filters, attributes)

    def read(self, id, attributes=dict()):
        response = self.api.connect("GET", id, {})

        return response

    def create(self, data):
        response = self.api.connect("PUT", "", data)

        _logger.debug("Requested Create with data {data}".format(data=data))

        return response

    def write(self, data):
        response = self.api.connect("PUT", "", data)

        _logger.debug("Requested Update with data {data}".format(data=data))

        return response

    def delete(self, id):
        payload = json.dumps({id})
        response = self.api.connect("DELETE", "", payload)

        _logger.debug("Requested Delete for ID {id}".format(id=id))

        return response
