from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductProductExporter(Component):
    _name = "bananas.product.product.exporter"
    _inherit = "bananas.record.exporter"
    _apply_on = ["bananas.binding.product.product"]


class ProductProductExporterMapper(Component):
    _name = "bananas.product.product.exporter.mapper"
    _inherit = "bananas.export.mapper"
    _apply_on = "bananas.binding.product.product"

    @mapping
    def compute_referencia(self, record):
        # Comprobación si ya existe el bananas_id, en caso de que exista
        # Si no existe se le va a tomar de una secuenca
        # que voy a crear de 20 bananas
        if record["bananas_id"]:
            return {"referencia": record["bananas_id"]}
        else:
            # aqui va el calculo con la secuencia
            referencia = self.env["ir.sequence"].next_by_code("bananas.product") or ""
            # sobreescribimos el valor para que no vaya generando eternamete los codigo
            return {"referencia": referencia}

    @mapping
    def compute_familia(self, record):
        if record["categ_id"].parent_id:
            return {
                "familia": record["categ_id"].parent_id.name,
                "subfamilia": record["categ_id"].name,
            }
        else:
            return {"familia": record["categ_id"].name}

    @mapping
    def compute_foto(self, record):
        if record["image_1920"]:
            return {
                "foto": self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                + "/web/image?model=product.template&id="
                + str(record["odoo_id"].id)
                + "&field=image_128"
            }

    @mapping
    def compute_unidadesbulto(self, record):
        if record["packaging_ids"]:
            res = {}
            for package in record["packaging_ids"]:
                if package.to_20bananas_bulto_1:
                    res.update(
                        {
                            "unidadbulto": package.name,
                            "unidadesxbulto": package.qty,
                            "vendobulto": 1,
                        }
                    )
                elif package.to_20bananas_bulto_2:
                    res.update(
                        {
                            "unidadbulto2": package.name,
                            "unidadesxbulto2": package.qty,
                            "vendobulto2": 1,
                        }
                    )
            return res

    @mapping
    def compute_nombre(self, record):
        return {"nombre": record["name"]}

    @mapping
    def compute_activo(self, record):
        return {"activo": record["sale_ok"]}

    @mapping
    def compute_precio(self, record):
        return {"precio": record["list_price"]}

    @mapping
    def compute_descripcion(self, record):
        return {"descripcion": record["description"]}

    @mapping
    def compute_codigosbarra(self, record):
        return {"codigosbarra": record["barcode"]}

    @mapping
    def compute_unidad(self, record):
        return {"unidad": record["uom_id"].name}
