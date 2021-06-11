#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Author: Guadaltech Soluciones Tecnológicas S.L.
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class SaleOrderExporter(Component):

    _name = "bananas.sale.order.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.sale.order"]


class SaleOrderExporterMapper(Component):

    _name = "bananas.sale.order.exporter.mapper"
    _inherit = "bananas.export.mapper"

    ##Aqui marcare como realizado el valor de servido

    @mapping
    def compute_idpedido(self, record):
        return {"idpedido": record["bananas_id"]}

    @mapping
    def compute_servido10(self, record):
        return {"servido10": "1"}
