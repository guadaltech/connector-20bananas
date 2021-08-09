from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ResPartnerExporter(Component):
    _name = "bananas.res.partner.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.res.partner"]


class ResPartnerExporterMapper(Component):
    _name = "bananas.res.partner.exporter.mapper"
    _inherit = "bananas.export.mapper"
    _apply_on = "bananas.binding.res.partner"

    @mapping
    def compute_codcliente(self, record):
        # Comprobación si ya existe el bananas_id, en caso de que exista
        # Si no existe se le va a tomar de una secuenca
        # que voy a crear de 20 bananas
        if record["bananas_id"]:
            return {"codcliente": record["bananas_id"]}
        else:
            # aqui va el calculo con la secuencia
            codigocliente = self.env["ir.sequence"].next_by_code("bananas.client") or ""
            # sobreescribimos el valor para que no vaya generando eternamete los codigos
            self.env["bananas.binding.res.partner"].search(
                [("id", "=", record["id"])]
            ).write({"bananas_id": codigocliente})
            return {"codcliente": codigocliente}

    @mapping
    def compute_nombrecliente(self, record):
        return {"nombrecliente": record["name"]}

    @mapping
    def compute_diasreparto(self, record):
        # esto aun no lo se como hacerlo deppende de lo que tenga el record
        diasreparto = "0000000"
        # Algoritmo para calcular el string de los dias de reparto
        for dia in record["delivery_days_ids"]:
            if int(dia.dayofweek) == 0:
                day_before = ""
                day2change = diasreparto[0:1]
                day_after = diasreparto[1 : len(diasreparto)]
            elif int(dia.dayofweek) == len(diasreparto):
                day_before = diasreparto[0 : len(diasreparto) - 1]
                day2change = diasreparto[len(diasreparto) : len(diasreparto)]
                day_after = ""
            else:
                day_before = diasreparto[0 : int(dia.dayofweek)]
                day2change = diasreparto[int(dia.dayofweek) : int(dia.dayofweek) + 1]
                day_after = diasreparto[int(dia.dayofweek) + 1 : len(diasreparto)]

            day2change = day2change.replace("0", "1")
            diasreparto = day_before + day2change + day_after
        return {"diasreparto": diasreparto}

    @mapping
    def compute_codcomercial(self, record):
        if record["user_id"]:
            user_id = self.env["bananas.binding.res.partner"].search(
                [("id", "=", record["user_id"].id)]
            )
            if user_id.bananas_id:
                return {"codcomercial": user_id.bananas_id}


class ResPartnerRatesExporter(Component):
    _name = "bananas.res.partner.pricelist.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.res.partner.pricelist"]


class ResPartnerRatesExporterMapper(Component):
    _name = "bananas.res.partner.pricelist.exporter.mapper"
    _inherit = "bananas.export.mapper"
    _apply_on = "bananas.binding.res.partner.pricelist"

    @mapping
    def compute_codtarifa(self, record):
        tarifa = record["property_product_pricelist"]
        tarifa_binding = self.env["bananas.binding.product.pricelist"].search(
            [("odoo_id", "=", tarifa.id)]
        )
        if tarifa_binding and tarifa_binding.bananas_id:
            return {"codtarifa": tarifa_binding.bananas_id}
        else:
            raise ValidationError(
                _(
                    "The Rate is no exported to 20bananas, "
                    "so we can't add the client to the rate"
                )
            )

    @mapping
    def compute_codcliente(self, record):
        client_binding = self.env["bananas.binding.res.partner"].search(
            [("odoo_id", "=", record["id"])]
        )
        if client_binding and client_binding.bananas_id:
            return {"codcliente": client_binding.bananas_id}
        else:
            raise ValidationError(
                _(
                    "The Client is no exported to 20bananas, "
                    "so we can't add the client to the rate"
                )
            )
