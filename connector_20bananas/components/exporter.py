import logging

from odoo import _

from odoo.addons.component.core import AbstractComponent

_logger = logging.getLogger(__name__)


class BananasExporter(AbstractComponent):
    """
    Generic exporter
    """

    _name = "bananas.exporter"
    _inherit = ["base.exporter", "base.bananas.component"]

    def _create(self, map_record):
        """

        :param binding:
        :param map_record:
        :return:
        """
        self.external_id = self.backend_adapter.create(map_record)
        if self.external_id:
            self.binding.write({"bananas_id": self.external_id[0]})

        return self.external_id

    def get_binding(self, record):
        current_bindings = self.env[self.model._name].search(
            [
                ("odoo_id", "=", record.id),
                ("backend_id", "=", self.backend_adapter.backend.id),
            ],
            limit=1,
        )

        if current_bindings:
            self.external_id = current_bindings.bananas_id
            self.binding = current_bindings
        else:
            self.binding = self.env[self.model._name].create(
                {"odoo_id": record.id, "backend_id": self.backend_adapter.backend.id}
            )

    def _update(self, map_record):
        """
        Update of the record on the external system.
        :param binding: Binding to export
        :param map_record: Data to export
        :return: Execution of the CRUD method.
        """
        current = self.backend_adapter.read(self.external_id)
        if not current:
            return _("Record does not exists in Navision")
        return self.backend_adapter.write(map_record)

    def _map_data(self, binding, mapper=None):
        """
        Maps an object into data values.
        :param binding: Object to convert
        :param mapper: Specfic export mapper to use, if is none it wil use export.mapper
        :return: Map of record
        """
        if not mapper:
            mapper = self.component(usage="export.mapper")

        return mapper.map_record(binding).values()

    def _run(self):
        """

        :return:
        """
        # if not self.binding.exists():
        #   return _('Record to export does no longer exists.')
        self.get_binding(self.record)

        map_record = self._map_data(self.binding)
        if not map_record:
            return _("Nothing to export")

        # Si hay un Id externo actualizamos, sino creamos
        if self.external_id:
            self._update(map_record)
        else:
            self.external_id = self._create(map_record)


class BananasRecordExporter(AbstractComponent):
    """
    Record exporter for single records
    """

    _name = "bananas.record.exporter"
    _inherit = "bananas.exporter"
    _usage = "record.exporter"

    def __init__(self, working_context):
        super(BananasRecordExporter, self).__init__(working_context)
        self.binding = None
        self.external_id = None

    def run(self, record, fields=None):
        """
        todo Darle lógica
        :param binding:
        :param fields:
        :return:
        """
        # todo Review use
        self.record = record

        result = self._run()
        return result
