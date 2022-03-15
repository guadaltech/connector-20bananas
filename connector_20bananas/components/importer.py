from logging import getLogger

from odoo.addons.component.core import AbstractComponent

_logger = getLogger(__name__)


class BananasImporter(AbstractComponent):

    _name = "bananas.importer"
    _inherit = ["base.importer", "base.bananas.component"]

    def get_binding(self):
        """
        Returns the internal binding for this object. Usually, this corresponds
        with the object being imported.
        """
        return self.binder.to_internal(self.external_id)

    def _update(self, binding, map_record):
        """
        Writes the data imported into the corresponding record in Odoo.
        """
        return binding.with_context(connector_no_export=True).write(map_record)

    def _create(self, map_record):
        """
        Creates the record based on the data imported and initializes the
        binding.
        """
        model = self.model.with_context(connector_no_export=True)
        record = model.create(map_record)
        return record

    def _import_record(self, data):
        """
        Imports the record into Odoo. This is a generic method that should
        work with all models. If needed, it is recommended that you inherit
        the methods inside this method.
        """
        record = self._map_data(data)
        record.update({"backend_id": self.backend_record.id})
        self._set_external_id(data)

        binding = self.get_binding()
        if binding:
            self._update(binding, record)
        else:
            binding = self._create(record)

        self.binder.bind(self.external_id, binding)

        return record

    def _map_data(self, data, mapper=None):
        """
        Maps a record based on the "data" present.
        """
        if not mapper:
            mapper = self.component(usage="import.mapper")

        return mapper.map_record(data).values()

    def _set_external_id(self, data):
        """
        This method assigns to "external_id" the value of the key used for a
        given object. This should be implemented to the given key for each
        import used.
        """
        mapper = self.component(usage="import.mapper")
        external_id = ""

        for attribute in mapper.get_primary_key_attributes():
            if attribute not in data:
                raise KeyError("No key found for this import")
            external_id += data[attribute]

        self.external_id = external_id


class BananasBatchImporter(AbstractComponent):
    """
    The role of a BatchImporter is to search for a list of
    items to import, then it can either import them directly or delay
    the import of each item separately.
    """

    _name = "bananas.batch.importer"
    _inherit = "bananas.importer"
    _usage = "batch.importer"

    def run(self, filters=None):
        """
        Runs the Batch Importer. This method will connect to the Navision API
        and iterate over the records returned by the SOAP entrypoint to
        import the records into Navision.
        """
        _logger.info(
            "Starting Batch Importer for model {model}".format(model=self.model._name)
        )

        attributes = {
            # Hacer un atributo configurable desde Odoo (para reducir la
            #  carga en el servidor Navision)
            "setSize": 0
        }
        datas = self.backend_adapter.search(attributes=attributes)

        for data in datas:
            try:
                self._import_record(data)
            except Exception:
                self.env.cr.rollback()

                _logger.error(
                    "Error found when attempting to import an object", exc_info=1
                )
